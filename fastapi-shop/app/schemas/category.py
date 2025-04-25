from pydantic import BaseModel

class Category(BaseModel):
    category_name: str

class CategoryRecord(Category):
    category_id: int

class CategoryCreate(Category):
    pass

class CategoryUpdate(Category):
    pass

class CategoryResponse(CategoryRecord):
    pass