FROM public.ecr.aws/lambda/python:3.12

RUN curl -fsSL \
      "https://download.postgresql.org/pub/repos/yum/keys/PGDG-RPM-GPG-KEY-RHEL" \
      -o /etc/pki/rpm-gpg/PGDG-RPM-GPG-KEY-RHEL \
    && rpm --import /etc/pki/rpm-gpg/PGDG-RPM-GPG-KEY-RHEL \
    && printf '%s\n' \
      '[pgdg16]' \
      'name=PostgreSQL 16 for RHEL 9 - $basearch' \
      'baseurl=https://download.postgresql.org/pub/repos/yum/16/redhat/rhel-9-$basearch' \
      'enabled=1' \
      'gpgcheck=1' \
      'gpgkey=file:///etc/pki/rpm-gpg/PGDG-RPM-GPG-KEY-RHEL' \
      > /etc/yum.repos.d/pgdg16.repo \
    && dnf -y install postgresql16 \
    && dnf clean all

ENV PATH="/usr/pgsql-16/bin:${PATH}"

COPY requirements.txt ${LAMBDA_TASK_ROOT}/
RUN python -m pip install --no-cache-dir -r ${LAMBDA_TASK_ROOT}/requirements.txt

COPY lmb/ ${LAMBDA_TASK_ROOT}/lmb/

CMD ["lmb.handler.handler"]