pipeline {
    agent any

    environment {
        IMAGE_NAME = "url-shortener"
        APP_PORT   = "5050"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    PYTHONPATH=. pytest tests/ -v --junitxml=tests/results.xml
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${IMAGE_NAME}:latest ."
                sh "docker tag ${IMAGE_NAME}:latest ${IMAGE_NAME}:${BUILD_NUMBER}"
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker-compose down
                    docker-compose up -d
                '''
            }
        }

        stage('Health Check') {
            steps {
                sh '''
                    sleep 10
                    curl -f http://localhost:${APP_PORT}/stats || exit 1
                '''
            }
        }
    }

    post {
        always {
            junit 'tests/results.xml'
        }
        success {
            echo "Deployment successful! App running at http://localhost:${APP_PORT}"
        }
        failure {
            sh 'docker-compose logs'
            echo "Pipeline failed! Check logs."
        }
    }
}
