FROM public.ecr.aws/lambda/python:3.12

RUN dnf -y install \
    https://download.postgresql.org/pub/repos/yum/reporpms/EL-9-$(uname -m)/pgdg-redhat-repo-latest.noarch.rpm \
    && dnf -qy module disable postgresql \
    && dnf -y install postgresql16 \
    && dnf clean all

ENV PATH="/usr/pgsql-16/bin:${PATH}"

COPY requirements.txt ${LAMBDA_TASK_ROOT}/
RUN python -m pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/requirements.txt

COPY backup/ ${LAMBDA_TASK_ROOT}/backup/

CMD ["lmb.handler.handler"]