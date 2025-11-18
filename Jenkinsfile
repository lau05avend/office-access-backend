pipeline {
    agent any

    environment {
        DOCKER_HOST = 'unix:///var/run/docker.sock'
    }

    stages {
        stage('Construir contenedores') {
            steps {
                sh 'docker compose build'
            }
        }

        stage('Ejecutar pruebas unitarias') {
            steps {
                sh 'docker compose run --rm backend pytest -v --cov=app --cov-report=term-missing'
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
