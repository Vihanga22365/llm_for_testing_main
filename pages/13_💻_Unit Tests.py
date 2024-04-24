import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_community.llms import OpenAI
from langchain_community.chat_models import ChatOpenAI
import os
from st_pages import hide_pages
from langchain_google_genai import ChatGoogleGenerativeAI
import pandas as pd



os.environ['OPENAI_API_KEY'] = st.secrets["OPENAI_API_KEY"]
GOOGLE_API_KEY = st.secrets["GOOGLE_API_KEY"]

st.set_page_config(
    initial_sidebar_state="collapsed",
    layout="wide"
)

hide_pages(
    "homepage"
)

 
if st.button('Back'):
    switch_page("API Tests")


st.title('Generate Unit Tests')

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

st.write('Please fill the below details to write the unit tests')

# template = """ 
# I want to generate selenium test script for below test case. Below I mentioned the test case and business requirement.\n
# Test case type - {testCaseType}\n
# Test case - {testCase}\n
# Business Requirement:\n
# User Story Name - {userStoryName}\n
# Main Business Functionality - {mainBusinessFunc}\n
# Sub Business Functionalites - {subBusinessFunc}\n
# Precondition - {precondition}\n
# Type of End Users - {endUsersType}\n
# Think you are a QA engineer. You need to mainly consider above mention test case and generate selenium script for {language} according to that testcase, as a professional QA engineer. When you write selenium script please follow coding best practices, coding standards, exception handling as a QA engineer.
# """

template = """ 
    Think you as the expert software engineer for write unit tests for a Spring Boot {springboot_version} project with Junit and Mockito. I want to generate unit tests for the below functions using Junit and Mockito. Below I mentioned the function.

    Input for Function - {input_for_function}

    Functions - {function}

    Denpendent Codes - {dependent_codes}

    Instructions -
        You're required to generate unit tests for a Spring Boot {springboot_version} project. Please pay close attention to the Spring Boot project version specified. Ensure that the unit test script you generate does not include deprecated methods.
        Identify all dependent codes files related to this operation. the corresponding code snippets are provided in the Dependent Codes section. When writing your code, ensure to consider the dependencies outlined in that section.
        Use JUnit as the testing framework. Do not utilize any other testing frameworks.
        Avoid using external dependencies other than JUnit itself.
        Utilize direct method invocation for accessing the controller method. Do not simulate an HTTP request or involve external layers such as the Spring Test framework.
        Generate unit test script with latest version of Mockito and Junit
        Make sure to identify all  conditional statements (if else conditions, switch statements) and try/catch blocks, if exist in the given function and write the unit test script with considering all of conditional statements (if else conditions, switch statements) and try/catch blocks for get 100% test coverage, including handling edge cases, error conditions, and all possible execution paths.

    Completely identify the above-given function, Denpendent Code and Instructions.
    The important thing is you need to include assert statements along with verification, when you are writing the unit tests.
    Think step by step and consider the above instructions and write the unit test for the above given function according to the above Instructions.
    Make sure to write unit test script with 100% test coverage. Don't skip any single code line in the given function for write unit test scripts.
    Implement detailed logging for debugging purposes.
    Only answer me with the code and nothing else.
    The important thing is you need to write only the unit test code. Please don't write any explanations, comments, or additional notes.
"""


# template = """ 
# I want to generate selenium test script for below test case. Below I mentioned the test case and business requirement.\n
# Test case type - {testCaseType}\n
# Test case - {testCase}\n
# Business Requirement:\n
# User Story Name - {userStoryName}\n
# Main Business Functionality - {mainBusinessFunc}\n
# Sub Business Functionalites - {subBusinessFunc}\n
# Precondition - {precondition}\n
# Type of End Users - {endUsersType}\n
# Additional Information - {additionalInfo}
# Already available functions (please use if applicable and these are only the existing functions): : {reusableFunc}n
# Instructions:  Develop a Selenium script in {language} to automate the positive test case described above.
# Adhere to coding best practices, coding standards, and implement robust exception handling.
# Use the web driver as defined.
# {instructions}
# Include waits effectively using explicit waits.
# Not required to write already implemented functions.
# Do not keep functions with only comments, assume the existence of appropriate UI components and implement the code as much as you can.
# If any existing functions are reused, indicate where they are used.



# """


on = st.toggle('Populate fields with a sample scenario')

if not on:

    uploaded_file = st.file_uploader("Choose an Excel file", type=['xlsx']) 

    def get_excel_file_content_as_binary(file_path):
        with open(file_path, "rb") as file:
            return file.read()

    file_path = 'template_files/Unit_Testing_Template.xlsx'

    excel_file_content = get_excel_file_content_as_binary(file_path)

    st.download_button(label="Download Unit Testing Code Template",
                    data=excel_file_content,
                    file_name="Unit_Testing_Template.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
else:
    uploaded_file = None

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file, engine='openpyxl')
        data = df.iloc[0]  # Assuming data for form defaults is in the first row

        with st.form('api_ts_gen'):
            st.text_input('Springboot Version', placeholder='Enter Springboot Version', value=data.iloc[0], key = 'springboot_version',help="Enter the Springboot Version here")
            st.text_input('Input For a Function', value=data.iloc[1], placeholder='Enter Input For a Function', key='input_for_function', help="Enter the inputs for the function to here")
            st.text_area('Function', value=data.iloc[2], placeholder='Enter the Function Code', key = 'functionCode',help="Please Enter the Function code here", height=500)
            st.text_area('Denpendent Codes', value=data.iloc[3], placeholder='Enter the Denpendent Codes', key='dependent_codes', help="Enter the Denpendent Codes here.", height=500)


            submitted = st.form_submit_button("Generate")
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")


elif on:
    with st.form('api_ts_gen'):
        
        func_code = """
            @PostMapping("employee")
            public ResponseEntity<ResponseDTO> createEmployee(@RequestBody  EmployeeDTO employeeDTO) throws UserExistException {
                EmployeeDTO savedEmployee = employeeService.createEmployee(employeeDTO);
                return ResponseEntity.status(HttpStatus.CREATED).body(new ResponseDTO(HttpStatus.CREATED, "Employee created successfully", savedEmployee));
            }
        """
        
        dependent_code = """
            EmployeeDTO.java:
            public class EmployeeDTO {
                private String employeeId;
                private String employeeFirstName;
                private String employeeLastName;
                private String employeePassword;
                private String employeeType;
            }
            
            -----------------------------------
            
            ResponseDTO.java:
            public class ResponseDTO {
                private HttpStatus status;
                private String message;
                private Object data;
            }
        """
        st.text_input('Springboot Version', placeholder='Enter Springboot Version', value="2.7.16", key = 'springboot_version',help="Enter the Springboot Version here")
        st.text_input('Input For a Function', value="employeeDTO", placeholder='Enter Input For a Function', key='input_for_function', help="Enter the inputs for the function to here")
        st.text_area('Function', value=func_code, placeholder='Enter the Function Code', key = 'functionCode',help="Please Enter the Function code here", height=500)
        st.text_area('Denpendent Codes', value=dependent_code, placeholder='Enter the Denpendent Codes', key='dependent_codes', help="Enter the Denpendent Codes to here.", height=500)
        submitted = st.form_submit_button("Generate")

else: 
    with st.form('api_ts_gen'):
        st.text_input('Springboot Version', placeholder='Enter Springboot Version', key = 'springboot_version',help="Enter the Springboot Version here")
        st.text_input('Input For a Function',  placeholder='Enter Input For a Function', key='input_for_function', help="Enter the inputs for the function to here")
        st.text_area('Function', placeholder='Enter the Function Code', key = 'functionCode',help="Please Enter the Function code here", height=500)
        st.text_area('Denpendent Codes', placeholder='Enter the Denpendent Codes', key='dependent_codes', help="Enter the Denpendent Codes to here.", height=500)
        
        submitted = st.form_submit_button("Generate")




if submitted: 
    ui_ts_template = PromptTemplate.from_template(template)
    ui_ts_template.input_variables = ['springboot_version', 'input_for_function', 'function', 'dependent_codes']

    formatted_prompt = ui_ts_template.format(
        springboot_version = st.session_state.springboot_version,
        input_for_function = st.session_state.input_for_function,
        function = st.session_state.functionCode,
        dependent_codes = st.session_state.dependent_codes
    )


    if model == 'GPT-3.5 Turbo':

        st.write('Using: '+model)

        llm = OpenAI(model_name= "gpt-3.5-turbo-0613", temperature = 0.1)

        if(len(formatted_prompt) != 0):
            response = llm(formatted_prompt)
            st.session_state['response_code'] = response

                    

    if model ==  'GPT-4': 
        st.write('Using: ' + model)

        llm = ChatOpenAI(model_name= "gpt-4", temperature = 0, model_kwargs={"seed": 10})

        if(len(formatted_prompt) != 0):
            response = llm.invoke(formatted_prompt)
            st.session_state['response_code'] = response.content
            

    if model ==  'Google Gemini Pro': 
        st.write('Using: ' + model)

        llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key = GOOGLE_API_KEY)

        if(len(formatted_prompt) != 0):
            response = llm.invoke(formatted_prompt)
            st.session_state['response_code'] = response.content

    if model == None:
        st.error('Please Select a LLM')


def describe_code_function(response, llm):

    full_prompt = f"""
        Generated Code : {response}

        Think you as the Expert Software Engineer, Understand above given unit testing code. 
        Think step by step and describe the code in detail.
        Give the code with adding description for each line of the code as comments.
    """
    if model == 'GPT-3.5 Turbo':
        llm = OpenAI(model_name= "gpt-3.5-turbo-0613", temperature = 0.1)
        response = llm(full_prompt)
        return response
    
    if model ==  'GPT-4':
        llm = ChatOpenAI(model_name= "gpt-4", temperature = 0, model_kwargs={"seed": 10})
        response = llm.invoke(full_prompt)
        return response.content
    
    if model ==  'Google Gemini Pro':
        llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key = GOOGLE_API_KEY)
        response = llm.invoke(full_prompt)
        return response.content
    

if 'response_code' in st.session_state:
    st.code(st.session_state['response_code'])

    # if st.session_state.language == 'Python':
    #     file_extension = 'py'
    # else:
    #     file_extension = 'java'
    file_extension = 'txt'

    filename = f"unit_testingcode.{file_extension}"
    
    code_to_download = str(st.session_state['response_code']) 
    
    col1, col2 = st.columns(2)

    with col1: 
        st.download_button(
            label="Export Code",
            data=code_to_download,
            file_name=filename,
            mime="text/plain",
            use_container_width=True
        )

    with col2: 
        describe_code = st.button(
            label="Describe the Code",
            use_container_width=True,
            key="describe_code"
        )


    if describe_code:
        full_description = describe_code_function(st.session_state['response_code'], model)
        st.code(full_description)

st.cache_data.clear()




