pipeline {
    agent any

    environment {
        DOCKER_HOST = 'unix:///var/run/docker.sock'
        CODECOV_TOKEN = credentials('codecov-token')
    }

    stages {
        stage('Verificar dependencías') {
            steps {
                sh '''
                    docker version
                    docker-compose version
                '''
            }
        }
        stage('Construir contenedores') {
            steps {
                sh 'docker-compose build'
            }
        }

        stage('Ejecutar pruebas unitarias') {
            steps {
                sh '''
                    docker-compose run --rm backend \
                    pytest -v --cov=app --cov-branch \
                    --cov-report=xml --cov-report=term-missing
                '''
            }
        }

        stage('Desplegar') {
            steps {
                sh 'docker-compose up -d'
            }
        }

        stage('Subir Coverage a Codecov') {
            steps {
                sh '''
                    # Descargar Codecov CLI
                    curl -Os https://cli.codecov.io/latest/linux/codecov
                    chmod +x codecov

                    # Subir el coverage.xml
                    ./codecov upload-process \
                        -t "$CODECOV_TOKEN" \
                        -f coverage.xml
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline terminado'
        }
    }
}