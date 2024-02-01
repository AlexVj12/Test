
echo 'Running server...'
gunicorn -k uvicorn.workers.UvicornWorker -w 4 Test.asgi:application