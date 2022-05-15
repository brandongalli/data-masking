import os
import csv
import itertools
from dataclasses import fields
from .schema import Customer


def lower_first(iterator):
    """Lowercase first line
    @param iterator: Iterator that the first line will be lowercased.
    """
    return itertools.chain([next(iterator).lower()], iterator)


def get_fields(data_class):
    """Get field names of data class.
    """
    return [field.name for field in fields(data_class)]


def get_min_max(data, field):
    """Get min, max, avg value/length of given data.
    @param data: list of object
    @field: attribute of object
    """
    if field == "id":
        return

    min = 1000000
    max = 0
    total = 0
    for row in data:
        value = getattr(row, field)
        if isinstance(value, str):
            length = len(value)
            min = length if length < min else min
            max = length if length > max else max
            total += length
        if isinstance(value, int) or isinstance(value, float):
            min = value if value < min else min
            max = value if value > max else max
            total += value

    return min, max, total/len(data)


def read_csv(file_path, data_class=Customer):
    """Read CSV and get average value of all numberic fields(except `id` field) & rows.
    @param file_path: Input file path.
    @param data_class: Inputed data class
    """
    if not os.path.exists(file_path):
        raise ValueError(f"File doesn't exists - {file_path}")
    result = []
    total = 0
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(lower_first(csvfile))
        for row in reader:
            obj = data_class(**row)
            result.append(obj)
            total += obj.total()

    return (result, total/len(result))


def write_csv(data, num_mask, field_names, file_path) -> None:
    """Write data to csv file.
    @param data: Data will be written in csv
    @param num_mask: Numberic data that will mask numeric fields of row.
    @field_names: CSV column names.
    @file_path: Output file path.
    """
    with open(file_path, "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        for row in data:
            writer.writerow(
                row.mask_values(num_mask=num_mask).__dict__
            )
