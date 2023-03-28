from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from api import Predictor, InputModel
app = FastAPI()

templates = Jinja2Templates(directory="Views")
app.mount("/Views", StaticFiles(directory="frontend"), name="views")
app.mount("/node_modules", StaticFiles(directory="node_modules"), name="modules")


@app.get('/', response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("Index.html", {"request": request})


@app.post('/predict')
async def predict(request: Request):
    try:
        data = await request.form()
        data = jsonable_encoder(data)
        data: InputModel = InputModel.InputModel.parse_obj(data)
        prediction = Predictor.predict_diabetes(data)
        result = ''
        if prediction == 0:
            result = 'Not Diabetes'
        elif prediction == 1:
            result = 'Diabetes'
        return templates.TemplateResponse("Index.html", {"request": request, "result": result})
    except Exception as e:
        return {'error': str(e)}
