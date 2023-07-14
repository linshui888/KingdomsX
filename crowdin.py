# Setup: Project Settings > Facets > Python
#        Or Right-click on "KingdomsX" project folder in Intellij > Add Framework Support > Python
#        After doing this, wait for indexing to finish.
# Run: Right-click anywhere in this file and click "Run File in Python Console"
# Used Python version: 3.11.2
# Used libs: https://pyyaml.org/wiki/PyYAMLDocumentation

import os

import yaml


# Pyyaml doesn't indent lists: https://github.com/yaml/pyyaml/issues/234
# Ain't not fucking way...
class CrowdinDumper(yaml.Dumper):
    def increase_indent(self, flow=False, indentless=False):
        return super(CrowdinDumper, self).increase_indent(flow, False)


def quotePaths(dumper, data):
    if "/" in data:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
    else:
        return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='')


yaml.add_representer(str, quotePaths)

crowdinFiles = []

guiSourcePath = r"core/src/main/resources/guis"
for subdir, _, files in os.walk(guiSourcePath):
    # Language file
    crowdinFiles.append({
        "source": f"/core/src/main/resources/en.yml",
        "translation": f"/resources/languages/%two_letters_code%/%two_letters_code%.yml"
    })

    subdir = subdir.replace('\\', '/')

    # GUIs
    for file in files:
        translationDir = subdir[len(guiSourcePath):]

        if file.endswith(".yml"):
            crowdinFiles.append({
                "source": subdir + '/' + file,
                "translation": f"/resources/languages/%two_letters_code%/guis{translationDir}/{file}"
            })
            print(f"{subdir}  -  {translationDir} - {file}")

with open(r'crowdin.yml', 'w') as file:
    file.write("# https://developer.crowdin.com/configuration-file/\n")
    file.write("# Automatically generated by crowdin.py, do not edit.\n\n")

    dumper = CrowdinDumper(stream=file, default_style=None,
                           default_flow_style=False,
                           canonical=False, indent=2, allow_unicode=True,
                           encoding='utf-8',
                           explicit_start=False, explicit_end=False, sort_keys=False,
                           width=None, line_break=None, version=None, tags=None
                           )

    data = dict(files=crowdinFiles)
    # yaml.dump(data=data, stream=file, Dumper=dumper)

    try:
        dumper.open()
        dumper.represent(data)
        dumper.close()
    finally:
        dumper.dispose()
