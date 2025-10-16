// frontend/src/components/IntakeForm/PersonalInfo.tsx
import React from 'react';
import { useFormContext } from 'react-hook-form';
import { useTranslation } from 'react-i18next';

const PersonalInfo: React.FC = () => {
  const { register, formState: { errors } } = useFormContext();
  const { t } = useTranslation();

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold">{t('personalInfo.title')}</h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">
            {t('personalInfo.firstName')}
          </label>
          <input
            type="text"
            {...register("firstName", { required: true })}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          />
          {errors.firstName && (
            <p className="mt-1 text-sm text-red-600">
              {t('validation.required')}
            </p>
          )}
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700">
            {t('personalInfo.lastName')}
          </label>
          <input
            type="text"
            {...register("lastName", { required: true })}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500"
          />
        </div>
      </div>

      {/* More fields for demographics, medical history, etc. */}
    </div>
  );
};

export default PersonalInfo;