package com.darkness.exception;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.http.server.reactive.ServerHttpRequest;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.ResponseStatus;
import org.springframework.web.bind.annotation.RestControllerAdvice;

import static org.springframework.http.HttpStatus.NOT_FOUND;

@RestControllerAdvice
class ControllerExceptionHandler {

        private static final Logger LOG = LoggerFactory.getLogger(ControllerExceptionHandler.class);

        @ResponseStatus(NOT_FOUND)
        @ExceptionHandler(NotFound.class)
        public @ResponseBody
        HttpErrorInfo handleNotFoundExceptions(ServerHttpRequest request, Exception ex) {

            return createHttpErrorInfo(NOT_FOUND, request, ex);
        }

        /*@ResponseStatus(UNPROCESSABLE_ENTITY)
        @ExceptionHandler(InvalidInputException.class)
        public @ResponseBody HttpErrorInfo handleInvalidInputException(ServerHttpRequest request, Exception ex) {

            return createHttpErrorInfo(UNPROCESSABLE_ENTITY, request, ex);
        }

        @ResponseStatus(NOT_IMPLEMENTED)
        @ExceptionHandler(InvalidInputException.class)
        public @ResponseBody HttpErrorInfo handleMissingException(ServerHttpRequest request, Exception ex) {

            return createHttpErrorInfo(NOT_IMPLEMENTED, request, ex);
        }*/

        private HttpErrorInfo createHttpErrorInfo(HttpStatus httpStatus, ServerHttpRequest request, Exception ex) {
            final String path = request.getPath().pathWithinApplication().value();
            final String message = ex.getMessage();

            LOG.debug("Returning HTTP status: {} for path: {}, message: {}", httpStatus, path, message);
            return new HttpErrorInfo(httpStatus, path, message);
        }
}

