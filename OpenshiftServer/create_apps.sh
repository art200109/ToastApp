PATH=$PATH:/opt/ocp/

oc new-project toast

apps=( menu login inventory order )
for app in "${apps[@]}"
do
    oc new-app https://github.com/art200109/ToastApp.git --context-dir=OpenshiftServer/Microservices/$app --name $app
    oc expose svc/$app
done

mongo_ip=$(dig +short toast-mongo.westeurope.cloudapp.azure.com)

sed "s/<<mongo_ip>>/$mongo_ip/g" ./toast-project.yml > ./toast-project_new.yml

oc apply -f ./toast-project_new.yml
