import re
from dataclasses import dataclass, fields

@dataclass
class Customer:
    """Represents a customer object
    Each customer has a unique id, full name, email,
    billing, and location.
    """
    id: str
    name: str
    email: str
    billing: float
    location: str

    def validate(self):
        """Validate fields
        Check if email is valid formation.
        Check if billing is valid float.
        """
        self.email = self.email.strip()
        try:
            self.billing = float(self.billing)
        except:
            self.billing = 0

        regex = re.compile(
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
        if not re.match(regex, self.email):
            raise ValueError(
                f"Email({self.email}) isn't valid for customer - {self.name}")

    def __post_init__(self):
        self.validate()

    def mask_values(self, num_mask=0):
        """Mask string fields and numeric fields(except id field).
        @param num_mask: Value that mask numeric fields.
        """
        for field in fields(self):
            if field.type == str:
                value = getattr(self, field.name)
                setattr(
                    self,
                    field.name,
                    re.sub(r'[a-zA-Z]', 'X', value)
                )
            elif field.type in [float, int] and field.name != 'id':
                setattr(self, field.name, num_mask)

        return self

    def total(self):
        """
        Return sum of numeric field except id field.
        """
        sum = 0
        for field in fields(self):
            if field.type in [int, float] and field.name != 'id':
                sum += getattr(self, field.name)

        return sum
