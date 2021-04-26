from pydantic import BaseModel, Field

class Counting(BaseModel):
    name : str  = Field(title= "The name of the string" ,regex = "^[a-z_]{3,15}$" )
    value : int  = Field (..., gt =0 , lt = 10, description= "The Value must be less than  10")

class ShowCounting(BaseModel):
    name : str
    value : int
    
    class Config():
        orm_mode = True