import { useCallback, useMemo, useState } from 'react';
import {
    ValidationRule,
    ValidationStateInfo,
    getValidationState,
    validateField
} from '../utils/validation';

export interface UseInputValidationOptions {
    rules: ValidationRule;
    initialValue?: string;
    validateOnChange?: boolean;
    validateOnBlur?: boolean;
}

export interface UseInputValidationReturn {
    value: string;
    setValue: (value: string) => void;
    validationState: ValidationStateInfo;
    isTouched: boolean;
    isValid: boolean;
    errorMessage?: string;
    errorCode?: string;
    handleChange: (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => void;
    handleBlur: () => void;
    handleFocus: () => void;
    reset: () => void;
    validate: () => ValidationStateInfo;
}

export function useInputValidation({
    rules,
    initialValue = '',
    validateOnChange = true,
    validateOnBlur = true
}: UseInputValidationOptions): UseInputValidationReturn {
    const [value, setValueState] = useState(initialValue);
    const [isTouched, setIsTouched] = useState(false);

    const validationState = useMemo(() => {
        return getValidationState(value, rules, isTouched);
    }, [value, rules, isTouched]);

    const setValue = useCallback((newValue: string) => {
        setValueState(newValue);
    }, []);

    const handleChange = useCallback((e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
        const newValue = e.target.value;
        setValue(newValue);

        if (validateOnChange) {
            setIsTouched(true);
        }
    }, [setValue, validateOnChange]);

    const handleBlur = useCallback(() => {
        setIsTouched(true);
    }, []);

    const handleFocus = useCallback(() => {
        // Focus handler for future enhancements
    }, []);

    const validate = useCallback(() => {
        const result = validateField(value, rules);
        return {
            state: result.isValid ? 'valid' : 'invalid',
            isValid: result.isValid,
            errorCode: result.errorCode,
            errorMessage: result.errorMessage
        };
    }, [value, rules]);

    const reset = useCallback(() => {
        setValue(initialValue);
        setIsTouched(false);
    }, [setValue, initialValue]);

    return {
        value,
        setValue,
        validationState,
        isTouched,
        isValid: validationState.isValid,
        errorMessage: validationState.errorMessage,
        errorCode: validationState.errorCode,
        handleChange,
        handleBlur,
        handleFocus,
        reset,
        validate
    };
}
