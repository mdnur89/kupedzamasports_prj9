# kupedzamasports_prj9

To run, first create conda environment

>$ conda create -n env-name --file requirements.txt
                    OR
>$ conda env create -n env-name --file environment.yml
                    OR
create conda environment then export the .yml:

>$ conda env export > environment.yml
                    
use the .yml file included to create an environment using any other provider of your choosing.

After environment activation, run the below to start the app:

>$ python manage.py makemigrations
 $ python manage.py migrate
 $ python manage.py runserver

NOTE THAT BUILD IS FAILING A PASS BUT RUNS
