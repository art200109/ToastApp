PATH=$PATH:/opt/ocp/

oc new-project toast

apps=( menu login inventory order )
for app in "${apps[@]}"
do
    oc new-app https://github.com/art200109/ToastApp.git --context-dir=OpenshiftServer/Microservices/$app --name $app
    oc expose svc/$app
done

oc apply -f ./toast-project.yml
