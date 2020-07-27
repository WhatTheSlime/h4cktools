import json
from path
import zipfile
import tarfile

'''
def extract(archive_path, output=None):
    """Extracts the archive and return the root archive directory.
    Only support zip and tar files

    Args:
        archive_path: path to archive to extract

    Returns:
        str: extracted archive folder path.
    """
    #: Name of the inside archive folder.
    archive_folder_name = None
    #: archive folder extractor
    extractor = None
    #: List of files names at archive's root.
    archive_files = None

    if not destination:
        destination = folder_path

    # Archive type is .zip
    if zipfile.is_zipfile(archive_path):
        extractor = zipfile.ZipFile(archive_path, "r")
        archive_files = extractor.namelist()

    # Archive type is .tar.gz
    elif tarfile.is_tarfile(archive_path):
        extractor = tarfile.open(archive_path, "r")
        archive_files = extractor.getnames()
    else:
        raise ValueError(f"Archive is not zip or tar.")

    #: list with all roots folders in the archive.
    roots = list(
        dict().fromkeys([name.split("/")[0] for name in archive_files])
    )

    # If there is only one root folder, it just exracts the archive.
    if len(roots) == 1 and roots[0] != "." and roots[0] != "..":
        archive_folder_name = roots[0]
        extractor.extractall(destination)

    # Else, it creates a folder named with cms name to extract archive.
    else:
        archive_folder_name = archive_name.split(".")[0]
        extractor.extractall(os.path.join(destination, archive_folder_name))
    
    extractor.close

    return archive_folder_name
'''