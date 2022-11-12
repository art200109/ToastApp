apps=( menu login inventory order )
for app in "${apps[@]}"
do
    oc delete all --selector app=$app
done