pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                sh 'echo "Building project..."'
                sh 'ls'
            }
        }

        stage('Test') {
            steps {
                sh 'echo "Running tests..."'
            }
        }

        stage('Deploy') {
            steps {
                sh 'echo "Deploying project..."'
            }
        }
    }
}
