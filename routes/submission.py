from fastapi import APIRouter, Request
import uuid
from uuid import UUID
from typing import List

from schemas.submission import SubmissionRequestBody
from utils.form.submission import Submission
from utils.utilities import log
from utils.response import ErrorResponse, ServerError, SuccessResponse, DataNotFoundError

data_submission_router = APIRouter(prefix="/data", tags=["Data Submission routes"])

submission = Submission()


@data_submission_router.post("/submission")
async def create_submission(submission_data: SubmissionRequestBody):
    try:
        print("submission", submission_data)
        _, error = submission.append_submission_db([submission_data])
        print(error)
        if error:
            return ErrorResponse(
                data=[], dev_msg=error, client_msg="Something went wrong while submission creation. Please try again after some time!!"
            )

        return SuccessResponse(data=submission_data, dev_msg="Data addition successful", client_msg="Data submitted successfully")

    except Exception as e:
        return ServerError(err=e, errMsg=str(e))


@data_submission_router.get("/submission")
async def get_all_submissions():
    try:
        submissions, error = submission.read_submission_db()
        if error:
            return ErrorResponse(
                data=[], dev_msg=error, client_msg="Something went wrong while fetching the submitted datas. Please try again after some time!!"
            )

        if len(submissions) == 0:
            return DataNotFoundError(dev_msg="No data available")

        return SuccessResponse(data=submissions, dev_msg="Forms fetched successfully", client_msg="Submitted Datas fetched successfully")

    except Exception as e:
        return ServerError(err=e, errMsg=str(e))


@data_submission_router.get("/submission/{submission_id}")
async def get_specific_submission(submission_id: str):
    try:
        submissions, error = submission.read_submission_db()
        if error:
            return ErrorResponse(
                data=[], dev_msg=error, client_msg="Something went wrong while fetching the submission. Please try again after some time!!"
            )

        for each_submission in submissions:
            print("EAH-",each_submission["submission_id"],"----", submission_id)
            print(each_submission["submission_id"] == submission_id)
            if each_submission["submission_id"] == submission_id:
                return SuccessResponse(data=each_submission, dev_msg="Data fetched successfully", client_msg="Data fetched successfully")

        return DataNotFoundError()

    except Exception as e:
        return ServerError(err=e, errMsg=str(e))


@data_submission_router.put("/submission/{submission_id}")
async def update_specific_submission(submission_id: str, updated_form: SubmissionRequestBody):
    try:
        submissions, error = submission.read_submission_db()
        if error:
            return ErrorResponse(
                data=[], dev_msg=error, client_msg="Something went wrong while updating the submission. Please try again after some time!!"
            )

        for index, each_form in enumerate(submissions):
            if each_form["submission_id"] == submission_id:
                submissions[index] = updated_form
                _, error = submission.write_submission_db(submissions)
                if error:
                    return ErrorResponse(
                        data=[], dev_msg=error, client_msg="Something went wrong while updating the submission. Please try again after some time!!"
                    )
                return SuccessResponse(data=updated_form, dev_msg="Update successful", client_msg="Data updated successfully")

        return DataNotFoundError()

    except Exception as e:
        return ServerError(err=e, errMsg=str(e))


@data_submission_router.delete("/submission/{submission_id}")
async def delete_specific_submission(submission_id: str):
    try:
        submissions, error = submission.read_submission_db()
        if error:
            return ErrorResponse(
                data=[], dev_msg=error, client_msg="Something went wrong while deleting the submission. Please try again after some time!!"
            )

        for index, each_form in enumerate(submissions):
            if each_form["submission_id"] == submission_id:
                del submissions[index]
                _, error = submission.write_submission_db(submissions)
                if error:
                    return ErrorResponse(
                        data=[], dev_msg=error, client_msg="Something went wrong while deleting the submission. Please try again after some time!!"
                    )
                return SuccessResponse(data=[], dev_msg="Delete successful", client_msg="Data deleted successfully")

        return DataNotFoundError()

    except Exception as e:
        return ServerError(err=e, errMsg=str(e))


@data_submission_router.get("/all/submission/{form_version_id}")
async def get_specific_submissions(form_version_id: str):
    try:
        submissions, error = submission.read_submission_db()
        if error:
            return ErrorResponse(
                data=[], dev_msg=error, client_msg="Something went wrong while fetching the submissions. Please try again after some time!!"
            )
            
        all_submissions = []

        for each_submission in submissions:
            if each_submission["form_version_id"] == form_version_id:
                all_submissions.append(each_submission)    
       
        
        return SuccessResponse(data=all_submissions, dev_msg="Fetched successfully", client_msg="Versioned submissions fetched successfully")

    except Exception as e:
        return ServerError(err=e, errMsg=str(e))

@data_submission_router.get("/total/submission/")
async def get_total_submission():
    try:
        submissions, error = submission.read_submission_db()
        if error:
            return ErrorResponse(
                data=[], dev_msg=error, client_msg="Something went wrong while fetching the submissions. Please try again after some time!!"
            )
            
        total_submissions = {}

        for each_submission in submissions:
            form_version = each_submission["form_version_id"]
            if form_version not in total_submissions:
                total_submissions[form_version] = 1
            else:
                total_submissions[form_version] = total_submissions[form_version]+1
                

        return SuccessResponse(data=total_submissions, dev_msg="Fetched successfully", client_msg="Versioned submissions fetched successfully")

    except Exception as e:
        return ServerError(err=e, errMsg=str(e))