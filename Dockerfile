FROM public.ecr.aws/lambda/python:3.9

COPY requirements.txt ${LAMBDA_TASK_ROOT}

RUN pip install -r requirements.txt

COPY .env ${LAMBDA_TASK_ROOT}/.env

COPY app/ ${LAMBDA_TASK_ROOT}/app

CMD ["app.main.lambda_handler"]