from fastapi import status, HTTPException

def find_post(all_posts, post_id):
    for index, post in enumerate(all_posts):
        if post["id"] == post_id:
            post = {
                "message": "Post found",
                "data": post
            }
            return index, post
    return -1, {
        "message": f"Post with ID: {post_id} was not found",
        "data": None
    }


def raise404Exception(post):
    if not post["data"]:
        post = {
            "message": f"No posts were found!",
            "data": None
        }
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=post)
    return post