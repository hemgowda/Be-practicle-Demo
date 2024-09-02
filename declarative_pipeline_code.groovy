pipeline {
    agent any
    stages {
        stage('one') {
            steps {
                echo 'Hi this is Hemanth from Be-practicle.'
            }
        }
        stage('Two') {
            steps {
                input('Do you want to proceed?')
            }
        }
        stage('Three') {
            when {
                not {
                    branch 'master'
                } 
            }
            steps {
                echo "Hello !"
            }
        }
        stage('Four') {
            parallel {
                stage('unit test') {
                    steps {
                        echo "Running the unit test ......."
                    } 
                } 
                stage('Integration test') {
                    agent {
                        docker {
                            image 'ubuntu'
                            args '-v /var/run/docker.sock:/var/run/docker.sock'  // Optional: Add arguments if needed
                        }
                    }
                    steps {
                        echo "Running the Integration test ......."
                    }
                }
            }
        }
    }
}
