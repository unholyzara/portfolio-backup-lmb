FROM public.ecr.aws/lambda/python:3.12

RUN dnf -y install postgresql \
    && dnf clean all

ENV PATH="/usr/pgsql-16/bin:${PATH}"

COPY requirements.txt ${LAMBDA_TASK_ROOT}/
RUN python -m pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/requirements.txt

COPY lmb/ ${LAMBDA_TASK_ROOT}/lmb/

CMD ["lmb.handler.handler"]