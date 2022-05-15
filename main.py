from customer.utils import read_csv, write_csv, get_fields, get_min_max
from customer.schema import Customer
customer = Customer


def main():
    customers, avg = read_csv("customers.csv", customer)
    
    write_csv(
        customers,
        avg,
        get_fields(customer),
        file_path="masked_clients.csv",
    )

    name_min, name_max, name_avg = get_min_max(customers, "name")
    billing_min, billing_max, billing_avg = get_min_max(customers, "billing")
    print("Report")
    print(f"Name: Max.{name_max}, Min.{name_min}, Avg.{name_avg}")
    print(f"Billing: Max.{billing_max}, Min.{billing_min}, Avg.{billing_avg}")

if __name__ == "__main__":
    main()
