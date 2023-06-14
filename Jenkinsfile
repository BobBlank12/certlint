pipeline {
  agent any
  stages {
    stage("Read the properties file") {
      steps {
        script {
          def props = readProperties file: 'VERSION'
          env.VERSION = props.VERSION
        }
      }
    }
    stage("Build the Docker image") {
      steps {
        echo 'Building the application...'
        sh 'docker stop certlint || exit 0'
        sh 'docker rm certlint || exit 0'
        sh 'rm -rf ./website/uploads/* || exit 0'
        sh 'docker build --tag certlint:${VERSION} .'
      }
    }
    stage("test") {
      steps {
        echo 'testing the application...'
      }
    }
    stage("Tag and Push the image to GCP Artifact registry") {
      // I got the idea to use a SECRET FILE from here:
      //  https://stackoverflow.com/questions/45355007/how-to-authenticate-with-a-google-service-account-in-jenkins-pipeline
      steps {
        echo 'Pushing the application to GCP Artifact Registry'
        sh 'docker tag certlint:${VERSION} us-central1-docker.pkg.dev/mygcp-385621/webapp/certlint:${VERSION}'
        script {
          withCredentials([file(credentialsId: 'mygcp-385621', variable: 'GC_KEY')]) {
            sh('gcloud auth activate-service-account --key-file=${GC_KEY}')
            sh('gcloud auth configure-docker us-central1-docker.pkg.dev')
            sh('docker push us-central1-docker.pkg.dev/mygcp-385621/webapp/certlint:${VERSION}')
          }
        }
      }
    }
    stage("Deploy to GKE"){
      steps {
        echo 'Deploying the container to GKE'
        script {
          withCredentials([file(credentialsId: 'mygcp-385621', variable: 'GC_KEY')]) {
            sh('gcloud auth activate-service-account --key-file=${GC_KEY}')
            sh('gcloud container clusters get-credentials gcp-lab-gke --region=us-central1')
            sh('kubectl apply -f certlint-gcp-k8s.yml')
          }
        }
      }
    }
  }
}


//gcloud auth activate-service-account --key-file=service_account.json
//gcloud config set project $project_id
//gcloud config set compute/zone $zone

//gcloud container clusters get-credentials gcp-lab-gke

//#!/bin/bash -xe
//gcloud container clusters get-credentials jenkins-cd
//kubectl cluster-info

//cd sample-app
//kubectl delete ns production  --grace-period=0 && sleep 180 || true
//kubectl create ns production
//kubectl --namespace=production apply -f k8s/production
//kubectl --namespace=production apply -f k8s/canary
//kubectl --namespace=production apply -f k8s/services
//kubectl --namespace=production scale deployment gceme-frontend-production --replicas=4

//for i in `seq 1 5`;do kubectl --namespace=production get service gceme-frontend; sleep 60;done

//export FRONTEND_SERVICE_IP=$(kubectl get -o jsonpath="{.status.loadBalancer.ingress[0].ip}"  --namespace=production services gceme-frontend)
//curl --retry 5 --retry-delay 5 http://$FRONTEND_SERVICE_IP/version | grep 1.0.0

//# Cleanup resources
//kubectl delete ns production
//sleep 120
//~                      
//