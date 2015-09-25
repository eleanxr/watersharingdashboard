echo "Entering Python virtual environment..."
source env/bin/activate

SETTINGS_MODULE='DjangoWebProject.settings.local'
echo "Settings module is $SETTINGS_MODULE"
export DJANGO_SETTINGS_MODULE=$SETTINGS_MODULE
