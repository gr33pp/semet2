# build_files.sh
# Install pip if it's not available
command -v pip > /dev/null 2>&1 || { 
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
    python get-pip.py
}

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate
