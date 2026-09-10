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
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'PYTHONPATH=. pytest'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t rewards-shop:ci .'
            }
        }
    }
}
