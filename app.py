import itertools

def generate_huge_list():
    username = "barelysorrybrosmyaminhasan"
    domain = "@gmail.com"
    filename = "full_email_database.txt"
    
    # 2^26 is approx 67 million lines
    print(f"জেনারেট হচ্ছে... এটি একটি বিশাল ফাইল হবে (প্রায় 2.5 GB)।")
    print("দয়া করে অপেক্ষা করুন, এতে বেশ কিছুক্ষণ সময় লাগতে পারে...")

    count = 0
    
    with open(filename, "w") as f:
        # map each character to lowercase and uppercase options
        # e.g., 'a' -> ('a', 'A')
        options = [(c.lower(), c.upper()) for c in username]
        
        # product generates all possible combinations (Cartesian product)
        for p in itertools.product(*options):
            email = "".join(p) + domain + "\n"
            f.write(email)
            count += 1
            
            # Progress update every 1 million
            if count % 1000000 == 0:
                print(f"{count} টি ইমেইল লেখা হয়েছে...")

    print(f"সম্পন্ন! মোট {count} টি ইমেইল '{filename}' ফাইলে সেভ করা হয়েছে।")

if __name__ == "__main__":
    generate_huge_list()