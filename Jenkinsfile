pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Create Python Environment') {
            steps {
                bat 'python -m venv .venv'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '.venv\\Scripts\\python.exe -m pip install --upgrade pip'
                bat '.venv\\Scripts\\python.exe -m pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'set PYTHONPATH=.&& .venv\\Scripts\\python.exe -m pytest'
            }
        }

        stage('Docker Build') {
            steps {
                bat 'docker build -t rewards-shop:ci .'
            }
        }
       stage('Docker Run') {
    steps {
        bat 'docker rm -f rewards-shop-ci 2>nul || exit /b 0'
        bat 'docker run -d --name rewards-shop-ci -p 5001:5000 rewards-shop:ci'
    }
         }
    }
}
