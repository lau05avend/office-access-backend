pipeline {
    agent {
        docker {
            image 'docker:28-cli'  // Imagen oficial con docker-cli + docker-compose
            args '-v /var/run/docker.sock:/var/run/docker.sock --user root'
        }
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