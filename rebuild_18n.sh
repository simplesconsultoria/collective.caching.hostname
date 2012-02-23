#! /bin/sh

I18NDOMAIN="collective.caching.hostname"
BASE_DIRECTORY="src/collective/caching/hostname"

# Synchronise the templates and scripts with the .pot.
./bin/i18ndude rebuild-pot --pot ${BASE_DIRECTORY}/locales/${I18NDOMAIN}.pot \
    --merge ${BASE_DIRECTORY}/locales/manual.pot \
    --create ${I18NDOMAIN} \
    ${BASE_DIRECTORY}

# Synchronise the resulting .pot with all .po files
for po in ${BASE_DIRECTORY}/locales/*/LC_MESSAGES/${I18NDOMAIN}.po; do
    ./bin/i18ndude sync --pot ${BASE_DIRECTORY}/locales/${I18NDOMAIN}.pot $po
done

# Report of errors and suspect untranslated messages
./bin/i18ndude find-untranslated ${BASE_DIRECTORY}
