import argparse
import libcovebods.api
import tempfile
import shutil
import json


def main():
    parser = argparse.ArgumentParser(description='Lib Cove BODS CLI')
    parser.add_argument("filename")
    parser.add_argument("--raw", help="show raw output from the library", action="store_true")

    args = parser.parse_args()

    cove_temp_folder = tempfile.mkdtemp(prefix='lib-cove-bods-cli-', dir=tempfile.gettempdir())
    try:
        result = libcovebods.api.bods_json_output(
            cove_temp_folder,
            args.filename,
            file_type='json'
        )
    finally:
        shutil.rmtree(cove_temp_folder)

    if not args.raw:
        del result['json_data']

    print(json.dumps(result, indent=4))


if __name__ == '__main__':
    main()
