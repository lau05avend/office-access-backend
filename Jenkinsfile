pipeline {
    agent any

    environment {
        DOCKER_HOST = 'unix:///var/run/docker.sock'
        CODECOV_TOKEN = credentials('codecov-token')
    }

    stages {

        stage('Verificar dependencias') {
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

        stage('Subir Coverage a Codecov') {
            when {
                expression { currentBuild.currentResult == 'SUCCESS' }
            }
            steps {
                sh '''
                    curl -Os https://cli.codecov.io/latest/linux/codecov
                    chmod +x codecov

                    ./codecov upload-process \
                        -f backend/coverage.xml \
                        -t "$CODECOV_TOKEN"
                '''
            }
        }

        stage('Desplegar') {
            when {
                expression { currentBuild.currentResult == 'SUCCESS' }
            }
            steps {
                sh 'docker-compose up -d'
            }
        }
    }

    post {
        always {
            sh 'docker-compose down --volumes --remove-orphans || true'
            echo 'Pipeline terminado'
        }
    }
}
