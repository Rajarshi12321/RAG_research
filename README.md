# Langchain_QA app Project

- [LinkedIn - Rajarshi Roy](https://www.linkedin.com/in/rajarshi-roy-learner/)
  
- [Github - Rajarshi Roy](https://github.com/Rajarshi12321/)

- [Medium - Rajarshi Roy](https://medium.com/@rajarshiroy.machinelearning)
  
- [Kaggle - Rajarshi Roy](https://www.kaggle.com/rajarshiroy0123/)
- [Mail - Rajarshi Roy](mailto:royrajarshi0123@gmail.com)
- [Personal-Website - Rajarshi Roy](https://rajarshi12321.github.io/rajarshi_portfolio/)


## Table of Contents

- [Langchain\_QA app Project](#langchain_qa-app-project)
  - [Table of Contents](#table-of-contents)
  - [About The Project](#about-the-project)
    - [For MLOPs tools:](#for-mlops-tools)
  - [Tech Stack](#tech-stack)
  - [Images](#images)
  - [Working with the code](#working-with-the-code)
  - [Contributing](#contributing)
  - [Contact](#contact)
  - [License](#license)


## About The Project

Welcome to the Langchain_QA app repository, a powerful tool built on Google Gemini technology. Our QA app is designed to efficiently implement the RAG (Retrieval-Augmented Generation) model, leveraging cutting-edge technologies including Langchain, Chainlit, and Gemini for lightning-fast query search and response generation.

Key Features:

1. RAG Model Integration: Our QA app seamlessly integrates the RAG model, a state-of-the-art approach that combines retrieval-based and generation-based methods for improved question answering.

2. Efficient Query Search: With the power of Langchain, Chainlit, and Gemini, our app ensures lightning-fast query search capabilities. Users can expect accurate and relevant responses to their queries in record time.

3. Modular Coding: The repository follows best practices of modular coding, ensuring clean and maintainable codebase. Developers can easily navigate through the code, making enhancements and modifications a breeze.

4. MLOps with GitHub Actions: We embrace MLOps principles by automating the deployment pipeline using GitHub Actions. Continuous integration and continuous deployment (CI/CD) ensure that changes are tested, integrated, and deployed seamlessly.

5. Docker Support: We provide a Dockerfile to create containers, enabling hassle-free deployment and ensuring consistency in dependencies across different environments. Docker simplifies the packaging and deployment of our app, making it easy to scale and manage.

6. AWS Integration: Deploy our QA app with ease on AWS EC2 and ECR. Utilize the power of AWS cloud infrastructure to host and scale your application. EC2 provides resizable compute capacity in the cloud, while ECR securely stores and manages Docker container images.

### For MLOPs tools:
I have used Github Actions for implementing CI/CD pipeline and AWS ECR for container registry of The Docker container and AWS EC2 for hosting it.

## Tech Stack
- Python
- Langchain
- Google Gemini
- Chainlit
- FAISS
- Docker
- Github Actions
- AWS ECR
- AWS EC2


## Images 

Langchain_QA Page : 
![image](https://github.com/Rajarshi12321/Langchain_QA/assets/94736350/29f8a163-142a-4c1c-84c0-971f61882e8b)



## Working with the code


I have commented most of the neccesary information in the respective files.

To run this project locally, please follow these steps:-

1. Clone the repository:

   ```shell
   git clone https://github.com/Rajarshi12321/Langchain_QA.git
   ```


2. **Create a Virtual Environment** (Optional but recommended)
  It's a good practice to create a virtual environment to manage project dependencies. Run the following command:
     ```shell
     conda create -p <Environment_Name> python==<python version> -y
     ```
     Example:
     ```shell
     conda create -p venv python=3.9 -y 
     ```
    Note:
    - It is important to use python=3.9 for proper use of Langchain or else you would get unexpecterd errors


3. **Activate the Virtual Environment** (Optional)
   Activate the virtual environment based on your operating system:
      ```shell
      conda activate <Environment_Name>/
      ```
      Example:
     ```shell
     conda activate venv/
     ```

4. **Install Dependencies**
   - Navigate to the project directory:
     ```
     cd [project_directory]
     ```
   - Run the following command to install project dependencies:
     ```
     pip install -r requirements.txt
     ```

   Ensure you have Python installed on your system (Python 3.9 or higher is recommended).<br />
   Once the dependencies are installed, you're ready to use the project.

5. Create a .env file in the root directory and add your Pinecone credentials as follows:
    ```shell  
    GOOGLE_API_KEY = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    ```


6. Run the Flask app: Execute the following code in your terminal.
   ```shell  
   chainlit run app.py -w
   ```
   

6. Access the app: Open your web browser and navigate to http://localhost:8000/ to use the House Price Prediction and Property Recommendation app.

## Contributing
I welcome contributions to improve the functionality and performance of the app. If you'd like to contribute, please follow these guidelines:

1. Fork the repository and create a new branch for your feature or bug fix.

2. Make your changes and ensure that the code is well-documented.

3. Test your changes thoroughly to maintain app reliability.

4. Create a pull request, detailing the purpose and changes made in your contribution.

## Contact

Rajarshi Roy - [royrajarshi0123@gmail.com](mailto:royrajarshi0123@gmail.com)



## License
This project is licensed under the MIT License. Feel free to modify and distribute it as per the terms of the license.

I hope this README provides you with the necessary information to get started with the road to Generative AI with Google Gemini and LlamaIndex.
