import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
import os
from st_pages import hide_pages
from langchain_google_genai import ChatGoogleGenerativeAI


st.set_page_config(
    initial_sidebar_state="collapsed",
    layout="wide"
)

hide_pages(
    "homepage"
)

 
if st.button('Back'):
    switch_page("API Test Case Gen")



os.environ['OPENAI_API_KEY'] = st.secrets["OPENAI_API_KEY"]
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]



st.title('Generate Test Scripts for Test Cases with Existing BDD Feature/ Scenario File.')

if 'model' in st.session_state:
    model = st.session_state.model
    st.write('Selected LLM: ',model)
    if st.button('Change the LLM',help='Change the LLM'):
        #switch_page('homepage')
        del st.session_state['model']
        model = st.selectbox(':red[Select the LLM Model to be used]',('GPT-3.5 Turbo', 'GPT-4','Google Gemini Pro'),key = 'llmModel', index = None)

        if model != None:
            st.session_state.model = model

else:
    model = st.selectbox(':red[Select the LLM Model to be used]',('GPT-3.5 Turbo', 'GPT-4','Google Gemini Pro'),key = 'llmModel', index = None)

    if model != None:
        st.session_state.model = model
    

if 'response' in st.session_state:
    tcResponse = st.session_state.response
    st.write('Please copy the test cases you want from the previously generated test cases below.')
    st.code(tcResponse)

st.write('Please fill the details below with respect to the test script you want to be generated')


scenario_template: str = """I want to generate cucumber scenario for below test case. Below I mention test case and API details.

Test case type - {testCaseType}\n
Tag name - {tagName} \n
Test case - {testCase}\n

Details:
API Endpoint - {apiEndpoint}\n
HTTP Method of API - {httpMethod}\n
Mandatory Header Parameters - {mandatoryHeaderParams}\n
Non-Mandatory Header Parameters - {nonMandatoryHeaderParams}\n
Mandatory Request Payload Parameters - {mandatoryRequestPayloadParameters}\n
Non-Mandatory Request Payload Parameters - {nonMandatoryRequestPayloadParameters}\n

Think you are a QA engineer. I need to genarate cucumber scenario for above test case, as a professional QA engineer. Please mainly focus about above mention test case and i need to genarate cucumber scenarion only for that test case. When you write cucumber scenario, please follow coding best practices, coding standards, exception handling as a QA engineer.
Only output the test scenario document.
"""

step_def_template: str = """
I want to generate {language} cucumber step definition for below cucumber feature file. Below I mention test case, API details and cucumber scenario.

Test case type - {testCaseType}\n
Tag name - {tagName} \n
Test cases - {testCase}\n

Details:
API Endpoint - {apiEndpoint}\n
HTTP Method of API - {httpMethod}\n
Mandatory Header Parameters - {mandatoryHeaderParams}\n
Non-Mandatory Header Parameters - {nonMandatoryHeaderParams}\n
Mandatory Request Payload Parameters - {mandatoryRequestPayloadParameters}\n
Non-Mandatory Request Payload Parameters - {nonMandatoryRequestPayloadParameters}\n
Cucumber scenario - {scenario}

Think you are a QA engineer. I need to genarate {language} cucumber step definition for above test case, as a professional QA engineer. Please mainly focus about above mention cucumber scenario and i need to genarate {language} cucumber step definition only for that cucumber scenario. Plase provide code in function body as much as possible. When you write java cucumber step definition, please follow coding best practices, coding standards, exception handling as a QA engineer."""

sample_step_def: str = """
**Feature: Scheduling a Meeting**

**Scenario: Schedule a Meeting with Valid RM and Customer**

**Given**
- A valid RM and customer exist in the system
- The API endpoint is https://localhost/api/v1/test
- The HTTP method of the API is POST
- The mandatory header parameters are Country code and business code
- The mandatory request payload parameters are Banker ID, Customer ID, Banker First Name, Customer First Name, Host Type, Start Time and End Time

**When**
- A meeting is scheduled with the valid RM and customer using the API

**Then**
- The API responds with a success status code
- The meeting is successfully scheduled in the system

**Examples:**
| Country code | Business code | Banker ID | Customer ID | Banker First Name | Customer First Name | Host Type | Start Time | End Time |
|---|---|---|---|---|---|---|---|---|
| IN | 1234 | 123456 | 654321 | John | Mary | Zoom | 2023-03-08T10:00:00 | 2023-03-08T11:00:00 |

**Scenario Outline:**

**Given**
- A valid RM and customer exist in the system
- The API endpoint is https://localhost/api/v1/test
- The HTTP method of the API is POST
- The mandatory header parameters are Country code and business code
- The mandatory request payload parameters are Banker ID, Customer ID, Banker First Name, Customer First Name, Host Type, Start Time and End Time

**When**
- A meeting is scheduled with the valid RM and customer using the API with the following data:

| Country code | Business code | Banker ID | Customer ID | Banker First Name | Customer First Name | Host Type | Start Time | End Time |
|---|---|---|---|---|---|---|---|---|
| <countryCode> | <businessCode> | <bankerId> | <customerId> | <bankerFirstName> | <customerFirstName> | <hostType> | <startTime> | <endTime> |

**Then**
- The API responds with a success status code
- The meeting is successfully scheduled in the system

**Examples:**
| countryCode | businessCode | bankerId | customerId | bankerFirstName | customerFirstName | hostType | startTime | endTime |
| IN | 1234 | 123456 | 654321 | John | Mary | Zoom | 2023-03-08T10:00:00 | 2023-03-08T11:00:00 |
| US | 5678 | 234567 | 765432 | Jane | Michael | Google Meet | 2023-03-09T12:00:00 | 2023-03-09T13:00:00 |
"""
on = st.toggle('Populate fields with a sample scenario')
if on:
    with st.form('api_ts_gen'):
        st.text_input('Test Case Type', placeholder='Enter Test Case Type', value= 'Positive Test Case',key = 'testCaseType',help="Enter the type of the test case here. Ex: Positive, Negative etc.")
        st.text_input('Tag Name', placeholder='Enter the name of the tag',value='DevEnv', key = 'tagName', help="Enter the tag name that is used to group the test cases")
        st.text_area('Test Cases', placeholder='Please Type the Test Case', value= 'Verify that a meeting can be scheduled successfully with a valid RM and customer.',key = 'testCase', height=150, help="Please Enter the Test Case to be tested here.")
        st.text_input('API Endpoint', placeholder='Enter the API Endpoint', value= 'https://localhost/api/v1/test',key = 'apiEndpoint', help="Please Enter the URL of the API to be tested in this field.")
        st.text_input('HTTP Method of API', placeholder='Enter the HTTP Method', value= 'POST',key = 'httpMethod', help="Please Enter the HTTP method of the API Ex: POST, GET, DELETE, PUT etc.")
        st.text_input('Mandatory Header Parameters', placeholder='',value= 'Country code and Business Code ', key = 'mandatoryHeaderParams')
        st.text_input('Non-Mandatory Header Parameters', placeholder='', value= 'UUID',key = 'nonMandatoryHeaderParams')
        st.text_input('Mandatory Request Payload Parameters', placeholder='',value= 'Banker ID, Customer ID, Banker First Name, Customer First Name, Host Type, Start Time and End Time ', key = 'mandatoryRequestPayloadParameters')
        st.text_input('Non-Mandatory Request Payload Parameters', placeholder='',value= 'Banker Last Name and Customer Last name ', key = 'nonMandatoryRequestPayloadParameters')
        st.text_area('Enter the Cucumber Feature File/ Scenario', placeholder='', value=sample_step_def, key = 'scenario', help="Copy the Cucumber Scenario File/ Feature File", height=500)
        st.selectbox('Required Language',('Python', 'Java'),key = 'language',index=1)
        submitted = st.form_submit_button("Generate")

else: 
    with st.form('api_ts_gen'):
        st.text_input('Test Case Type', placeholder='Enter Test Case Type', key = 'testCaseType',help="Enter the type of the test case here. Ex: Positive, Negative etc.")
        st.text_input('Tag Name', placeholder='Enter the name of the tag', key = 'tagName', help="Enter the tag name that is used to group the test cases")
        st.text_area('Test Cases', placeholder='Please Type the Test Case', key = 'testCase', help="Please Enter the Test Case to be tested here.", height=150)
        st.text_input('API Endpoint', placeholder='Enter the API Endpoint', key = 'apiEndpoint', help="Please Enter the URL of the API to be tested in this field.")
        st.text_input('HTTP Method of API', placeholder='Enter the HTTP Method', key = 'httpMethod', help="Please Enter the HTTP method of the API Ex: POST, GET, DELETE, PUT etc.")
        st.text_input('Mandatory Header Parameters', placeholder='', key = 'mandatoryHeaderParams')
        st.text_input('Non-Mandatory Header Parameters', placeholder='', key = 'nonMandatoryHeaderParams')
        st.text_input('Mandatory Request Payload Parameters', placeholder='', key = 'mandatoryRequestPayloadParameters')
        st.text_input('Non-Mandatory Request Payload Parameters', placeholder='', key = 'nonMandatoryRequestPayloadParameters')
        st.text_area('Enter the Cucumber Feature File/ Scenario', placeholder='', key = 'scenario', help="Copy the Cucumber Scenario File/ Feature File", height=500)
        st.selectbox('Required Language',('Python', 'Java'),key = 'language',index=1)
        submitted = st.form_submit_button("Generate")

if submitted: 

    cucumber_td_template = PromptTemplate.from_template(step_def_template)
    cucumber_td_template.input_variables=['testCaseType','tagName','testCase','apiEndpoint','apiName','httpMethod','endUserType','mainBusinessObjective','subBusinessObjective','mandatoryHeaderParams','nonMandatoryHeaderParams','mandatoryRequestPayloadParameters','nonMandatoryRequestPayloadParameters','mandatoryResponsePayloadParameters','nonMandatoryResponsePayloadParameters','language','scenario']

    cucumber_step_formatted_prompt = cucumber_td_template.format(
        testCaseType = st.session_state.testCaseType,
        tagName = st.session_state.tagName,
        testCase = st.session_state.testCase,
        apiEndpoint = st.session_state.apiEndpoint,
        httpMethod = st.session_state.httpMethod,
        # mainBusinessObjective = st.session_state.mainBusinessObjective,
        # subBusinessObjective = st.session_state.subBusinessObjective,
        # testScenarioCombination = st.session_state.testScenarioCombination,
        mandatoryHeaderParams = st.session_state.mandatoryHeaderParams,
        nonMandatoryHeaderParams = st.session_state.nonMandatoryHeaderParams,
        mandatoryRequestPayloadParameters = st.session_state.mandatoryRequestPayloadParameters,
        nonMandatoryRequestPayloadParameters = st.session_state.nonMandatoryRequestPayloadParameters,
        # mandatoryResponsePayloadParameters = st.session_state.mandatoryResponsePayloadParameters,
        # nonMandatoryResponsePayloadParameters = st.session_state.nonMandatoryResponsePayloadParameters,
        language = st.session_state.language,
        scenario = st.session_state.scenario
            )


    if model == 'GPT-3.5 Turbo':

        st.write('Using: '+model)

        llm = OpenAI(model_name= "gpt-3.5-turbo-0613", temperature = 0.5)

        if(len(cucumber_step_formatted_prompt) != 0):
            response = llm(cucumber_step_formatted_prompt)
            st.code(response)
            if 'response' in st.session_state:
                del st.session_state['response']

    if model ==  'GPT-4': 
        st.write('Using: ' + model)

        llm = ChatOpenAI(model_name= "gpt-4", temperature = 0, model_kwargs={"seed": 10})

        if(len(cucumber_step_formatted_prompt) != 0):
            response = llm.invoke(cucumber_step_formatted_prompt)
            st.code(response.content)
            if 'response' in st.session_state:
                del st.session_state['response']
            
        

    if model ==  'Google Gemini Pro': 
        st.write('Using: ' + model)

        llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key = GOOGLE_API_KEY)

        if(len(cucumber_step_formatted_prompt) != 0):
            response = llm.invoke(cucumber_step_formatted_prompt)
            st.code(response.content)
            if 'response' in st.session_state:
                del st.session_state['response']
            


    if model == None:
        st.error('Please Select a LLM')
