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
                        branch "master"
                } 
            }
            steps{
                echo "Hello !"
            }
        }
        stage('Four') {
            parallel {
                stage('unit test') {
                        steps{
                                echo "Running the unit test ......."
                        } 
                } 
                stage('Integration test'){
                    agent{
                        docker{
                            reuseNode false
                            image 'ubuntu'
                        }
                    }
                    steps{
                        echo "Running the Integration test ......."
                    }
            }
        }
    }
}
}
