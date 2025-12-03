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
                    docker-compose run --rm \
                    -v $(pwd):/workspace \
                    backend bash -c "cd /app && pytest -v --cov=. --cov-branch \
                    --cov-report=xml:/workspace/coverage.xml --cov-report=term-missing"
                '''
            }
        }

        stage('Subir Coverage a Codecov') {
            when {
                expression { currentBuild.currentResult == 'SUCCESS' }
            }
            steps {
                sh '''
                    echo "=== Verificando coverage.xml ==="
                    ls -la /workspace/coverage.xml
                    head -n 20 /workspace/coverage.xml

                    # Descargar Codecov CLI si no existe
                    if [ ! -f codecov ]; then
                        curl -Os https://cli.codecov.io/latest/linux/codecov
                        chmod +x codecov
                    fi

                    # Subir coverage
                    ./codecov upload-process \
                        -f /workspace/coverage.xml \
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
