pipeline {
    
    agent any
     environment {
        PROJECT_ID = 'qwiklabs-gcp-00-c5b741258cb0'
        CLUSTER_NAME = 'shop-cluster'
        LOCATION = 'us-west1-b'
        CREDENTIALS_ID = 'qwiklabs-gcp-00-c5b741258cb0'
    }     
    stages {

        stage("build") {
            
            //outlines the steps to be used e.g pip install; simply steps on a command line.
            steps {
                echo 'building the application'
            }
        }
        
        stage("test") {

            steps {
                echo 'testing the application'
               //Example of a command to run
            }
        }
       
        stage("deploy") {

            steps {
                echo 'deploying the application'
            }
        }
        
    }
}
