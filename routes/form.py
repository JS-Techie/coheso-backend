from fastapi import APIRouter, Request
import uuid, json, re
from uuid import UUID
from typing import List

from schemas.form import FormDataRequestBody
from utils.form.form import Form
from utils.utilities import log
from datetime import datetime
from utils.response import ErrorResponse, ServerError, SuccessResponse, DataNotFoundError

form_builder_router = APIRouter(prefix="/build", tags=["Form routes"])

form = Form()


@form_builder_router.post("/form")
async def create_form(form_data: List[FormDataRequestBody]):
    try:
        previous_forms, error = form.read_form_db()
        for each_form in previous_forms:
            if each_form['form_version_id'] == form_data[0].form_version_id:
                return ErrorResponse(
                data=[], dev_msg="form version Id conflict", client_msg="Version Name Already Exists. Try with a Different version name."
                )
        _, error = form.append_form_db(form_data)
        if error:
            return ErrorResponse(
                data=[], dev_msg=error, client_msg="Something went wrong while form creation. Please try again after some time!!"
            )

        return SuccessResponse(data=form_data, dev_msg="Form addition successful", client_msg="Form submitted successfully")

    except Exception as e:
        return ServerError(err=e, errMsg=str(e))


@form_builder_router.get("/form")
async def get_all_forms():
    try:
        forms, error = form.read_form_db()
        if error:
            return ErrorResponse(
                data=[], dev_msg=error, client_msg="Something went wrong while fetching the forms. Please try again after some time!!"
            )

        if len(forms) == 0:
            return DataNotFoundError(dev_msg="No data available")

        return SuccessResponse(data=forms, dev_msg="Forms fetched successfully", client_msg="Forms fetched successfully")

    except Exception as e:
        return ServerError(err=e, errMsg=str(e))
    
@form_builder_router.get("/latest/form")
async def get_all_latest_version_forms():
    try:
        forms, error = form.read_form_db()
        if error:
            return ErrorResponse(
                data=[], dev_msg=error, client_msg="Something went wrong while fetching the forms. Please try again after some time!!"
            )
            
        grouped_forms = {}
        format_string = "%a %b %d %Y %H:%M:%S GMT%z" 

        for each_form in forms:
            print(len(forms))
            form_id = each_form["form_id"]
            if form_id not in grouped_forms:
                grouped_forms[form_id] = each_form
            else:
                if datetime.strptime(re.sub(r' \([A-Za-z ]+\)', '', grouped_forms[form_id]['created_on']), format_string).timestamp() < datetime.strptime(re.sub(r' \([A-Za-z ]+\)', '', each_form['created_on']), format_string).timestamp():
                    grouped_forms[form_id] = each_form

        latest_version_forms = []
        for key in grouped_forms:
            latest_version_forms.append(grouped_forms[key])
            
        print(grouped_forms)
            
        if len(forms) == 0:
            return DataNotFoundError(dev_msg="No data available")

        return SuccessResponse(data=latest_version_forms, dev_msg="Forms fetched successfully", client_msg="Forms fetched successfully")

    except Exception as e:
        return ServerError(err=e, errMsg=str(e))


@form_builder_router.get("/form/{form_id}")
async def get_specific_form(form_id: str):
    try:
        forms, error = form.read_form_db()
        if error:
            return ErrorResponse(
                data=[], dev_msg=error, client_msg="Something went wrong while fetching the form. Please try again after some time!!"
            )
        
        for each_form in forms:
            if each_form["form_id"] == form_id:
                return SuccessResponse(data=each_form, dev_msg="Form fetched successfully", client_msg="Form fetched successfully")

        return DataNotFoundError()

    except Exception as e:
        return ServerError(err=e, errMsg=str(e))


@form_builder_router.put("/form/{form_version_id}")
async def update_specific_form(form_version_id: str, updated_form: FormDataRequestBody):
    try:
        forms, error = form.read_form_db()
        if error:
            return ErrorResponse(
                data=[], dev_msg=error, client_msg="Something went wrong while updating the form. Please try again after some time!!"
            )

        for index, each_form in enumerate(forms):
            if each_form["form_version_id"] == form_version_id:
                forms[index] = updated_form
                _, error = form.write_form_db(forms)
                if error:
                    return ErrorResponse(
                        data=[], dev_msg=error, client_msg="Something went wrong while updating the form. Please try again after some time!!"
                    )
                return SuccessResponse(data=updated_form, dev_msg="Update successful", client_msg="Data updated successfully")

        return DataNotFoundError()

    except Exception as e:
        return ServerError(err=e, errMsg=str(e))


@form_builder_router.delete("/form/{form_version_id}")
async def delete_specific_form(form_version_id: str):
    try:
        forms, error = form.read_form_db()
        if error:
            return ErrorResponse(
                data=[], dev_msg=error, client_msg="Something went wrong while deleting the form. Please try again after some time!!"
            )

        for index, each_form in enumerate(forms):
            if each_form["form_version_id"] == form_version_id:
                del forms[index]
                _, error = form.write_form_db(forms)
                if error:
                    return ErrorResponse(
                        data=[], dev_msg=error, client_msg="Something went wrong while deleting the form. Please try again after some time!!"
                    )
                return SuccessResponse(data=[], dev_msg="Delete successful", client_msg="Data deleted successfully")

        return DataNotFoundError()

    except Exception as e:
        return ServerError(err=e, errMsg=str(e))


# @form_builder_router.get("/form/version/all")
# async def get_versioned_forms():
    try:
        forms, error = form.read_form_db()
        if error:
            return ErrorResponse(
                data=[], dev_msg=error, client_msg="Something went wrong while fetching the forms. Please try again after some time!!"
            )

        grouped_forms = {}

        for each_form in forms:
            version = each_form["version"]
            if version not in grouped_forms:
                grouped_forms[version] = []
            grouped_forms[version].append(each_form)

        return SuccessResponse(data=grouped_forms, dev_msg="Fetched successfully", client_msg="Versioned forms fetched successfully")

    except Exception as e:
        return ServerError(err=e, errMsg=str(e))

@form_builder_router.get("/version/form/{form_id}")
async def get_versioned_forms(form_id : str):
    try:
        forms, error = form.read_form_db()
        if error:
            return ErrorResponse(
                data=[], dev_msg=error, client_msg="Something went wrong while fetching the forms. Please try again after some time!!"
            )

        versioned_forms=[]
        
        for each_form in forms:
            if each_form["form_id"] == form_id:
                versioned_forms.append(each_form)
                
        if len(versioned_forms) == 0:
            return DataNotFoundError()
        
        return SuccessResponse(data=versioned_forms, dev_msg="Fetched successfully", client_msg="Versioned forms fetched successfully")

    except Exception as e:
        return ServerError(err=e, errMsg=str(e))