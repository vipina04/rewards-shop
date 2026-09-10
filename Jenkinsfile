pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'set PYTHONPATH=.&& pytest'
            }
        }

        stage('Docker Build') {
            steps {
                bat 'docker build -t rewards-shop:ci .'
            }
        }
    }
}
