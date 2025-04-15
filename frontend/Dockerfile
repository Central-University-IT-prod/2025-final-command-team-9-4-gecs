FROM node:20-slim AS base

ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN npm i -g pnpm@10

WORKDIR /app

FROM base AS build
COPY pnpm-lock.yaml /app
RUN pnpm fetch
COPY . /app
RUN pnpm install -r --offline
RUN pnpm run build

FROM base AS runner
COPY --from=build /app/node_modules /app/node_modules
COPY --from=build /app/build /app/build

# Костыль
RUN echo '#!/bin/sh\ncp -r /app/build/* /app/dist/\necho "Build artifacts copied to /app/dist"' > /app/init.sh
RUN chmod +x /app/init.sh

ENTRYPOINT ["/app/init.sh"]
