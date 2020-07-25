import re

#: Generic regex to extract a version
version_regex = r"((\d+)\.(\d+)(\.(\d+))?(\.(\d+))?)"


def extract(string):
    """Extract a version from a generic string.

    Args:
        string (str): string that contains a version.
    """
    match = re.search(version_regex, string)
    return match.group(1) if match else None

class Version:
    """Object parsing versions"""
    def __init__(self, version):
        if not isinstance(version, str):
            raise TypeError(f"'{version}' type is not str")
        self.nums = [int(n) for n in version.split(".")]

    def __eq__(self, other):
        if len(self) != len(other):
            return False

        for i in range(0, len(self)):
            if self.nums[i] != other.nums[i]:
                return False
        return True

    def __lt__(self, other):
        for i in range(0, len(min(self.nums, other.nums, key=len))):
            if self.nums[i] < other.nums[i]:
                return True
            if self.nums[i] > other.nums[i]:
                return False
        return False

    def __le__(self, other):
        if self == other:
            return True
        return self < other

    def __len__(self):
        return len(self.nums)

    def __repr__(self):
        return ".".join([str(num) for num in self.nums])