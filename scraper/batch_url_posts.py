import os


posts_dkk = open('instagram_posts.txt', 'r')
post_list = posts_dkk.read().split("\n")

# batch each n post
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

n = 30
batch_post = list(chunks(post_list, n))

if not os.path.exists('batch'):
    os.makedirs('batch')

for i, batch in enumerate(batch_post):
    for post in batch:
        if post:
            with open(f"batch/{i}.txt", "a") as output:
                output.write(post + "\n")