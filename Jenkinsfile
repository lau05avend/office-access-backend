pipeline {
    agent any

    environment {
        DOCKER_HOST = 'unix:///var/run/docker.sock'
    }

    stages {

        stage('Instalar dependencias backend') {
            steps {
                dir('backend') {
                    sh 'pip install -r requirements.txt'
                }
            }
        }

        stage('Ejecutar pruebas unitarias') {
            steps {
                dir('backend') {
                    sh 'pytest -v --cov=app --cov-report=term-missing'
                }
            }
        }

        stage('Construir contenedores') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Desplegar') {
            steps {
                sh 'docker compose up -d'
            }
        }
    }

    post {
        always {
            echo 'Pipeline terminado'
        }
    }
}
