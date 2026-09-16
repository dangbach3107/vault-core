// Generated from contracts/openapi.json. Do not edit.
export interface paths {
    "/api/v1/companies": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** List Companies */
        get: operations["list_companies"];
        put?: never;
        /** Create Company */
        post: operations["create_company"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/companies/{company_id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get Company */
        get: operations["get_company"];
        /** Update Company */
        put: operations["update_company"];
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/companies/{company_id}/preview/{layer}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Preview Company */
        get: operations["preview_company"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/health": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Check that the API is responding
         * @description Liveness only. Does not check PostgreSQL or external providers.
         */
        get: operations["get_health"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/rooms": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** List Rooms */
        get: operations["list_rooms"];
        put?: never;
        /** Create Room */
        post: operations["create_room"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/rooms/{room_id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get Room */
        get: operations["get_room"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/rooms/{room_id}/documents": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Upload Document */
        post: operations["upload_document"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/rooms/{room_id}/documents/{document_id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get Document */
        get: operations["get_document"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/rooms/{room_id}/documents/{document_id}/versions": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Upload Version */
        post: operations["upload_version"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/rooms/{room_id}/documents/{document_id}/versions/{number}/content": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get Content */
        get: operations["get_document_content"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
}
export type webhooks = Record<string, never>;
export interface components {
    schemas: {
        /** AnonymousPreview */
        AnonymousPreview: {
            /** Alias */
            alias: string;
            deal_type: components["schemas"]["DealType"] | null;
            /** Employee Band */
            employee_band: string | null;
            /**
             * Layer
             * @default 1
             */
            layer: number;
            /**
             * Notice
             * @default Bản xem trước nội bộ; cần người duyệt nguy cơ nhận diện trước khi chia sẻ.
             */
            notice: string;
            region: components["schemas"]["Region"] | null;
            /** Revenue Band Vnd */
            revenue_band_vnd: string | null;
            sector: components["schemas"]["Sector"] | null;
        };
        /** ApiError */
        ApiError: {
            /** Detail */
            detail: string;
        };
        /** Body_upload_document */
        Body_upload_document: {
            /** File */
            file: string;
            folder: components["schemas"]["Folder"];
            /**
             * Note
             * @default
             */
            note: string;
            /** Title */
            title: string;
        };
        /** Body_upload_version */
        Body_upload_version: {
            /** File */
            file: string;
            /**
             * Note
             * @default
             */
            note: string;
        };
        /** CompanyInput */
        "CompanyInput-Input": {
            address?: components["schemas"]["Fact_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_1___MaxLen_max_length_2000_____"];
            company_name: components["schemas"]["Fact_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_1___MaxLen_max_length_200_____"];
            customer_groups?: components["schemas"]["Fact_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_1___MaxLen_max_length_2000_____"];
            deal_type?: components["schemas"]["Fact_DealType_"];
            decision_maker?: components["schemas"]["Fact_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_1___MaxLen_max_length_2000_____"];
            description?: components["schemas"]["Fact_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_1___MaxLen_max_length_2000_____"];
            employees?: components["schemas"]["Fact_Annotated_int__FieldInfo_annotation_NoneType__required_True__metadata__Ge_ge_0___Le_le_10000000_____"];
            /** Financials */
            financials?: components["schemas"]["FinancialYear-Input"][];
            founded_year?: components["schemas"]["Fact_Annotated_int__FieldInfo_annotation_NoneType__required_True__metadata__Ge_ge_1800___Le_le_2100_____"];
            funds_destination?: components["schemas"]["Fact_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_1___MaxLen_max_length_2000_____"];
            objectives?: components["schemas"]["Fact_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_1___MaxLen_max_length_2000_____"];
            permitted_use?: components["schemas"]["Fact_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_1___MaxLen_max_length_2000_____"];
            region?: components["schemas"]["Fact_Region_"];
            sector?: components["schemas"]["Fact_Sector_"];
            shareholders?: components["schemas"]["Fact_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_1___MaxLen_max_length_2000_____"];
            source_url?: components["schemas"]["Fact_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_8___MaxLen_max_length_2000____PydanticGeneralMetadata_pattern__https_____"];
            stake_percent?: components["schemas"]["Fact_Annotated_Decimal__FieldInfo_annotation_NoneType__required_True__metadata__Ge_ge_0___Le_le_100____PydanticGeneralMetadata_decimal_places_2_____-Input"];
            tax_id?: components["schemas"]["Fact_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_3___MaxLen_max_length_30_____"];
            technology?: components["schemas"]["Fact_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_1___MaxLen_max_length_2000_____"];
        };
        /** CompanyInput */
        "CompanyInput-Output": {
            address?: components["schemas"]["Fact_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_1___MaxLen_max_length_2000_____"];
            company_name: components["schemas"]["Fact_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_1___MaxLen_max_length_200_____"];
            customer_groups?: components["schemas"]["Fact_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_1___MaxLen_max_length_2000_____"];
            deal_type?: components["schemas"]["Fact_DealType_"];
            decision_maker?: components["schemas"]["Fact_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_1___MaxLen_max_length_2000_____"];
            description?: components["schemas"]["Fact_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_1___MaxLen_max_length_2000_____"];
            employees?: components["schemas"]["Fact_Annotated_int__FieldInfo_annotation_NoneType__required_True__metadata__Ge_ge_0___Le_le_10000000_____"];
            /** Financials */
            financials?: components["schemas"]["FinancialYear-Output"][];
            founded_year?: components["schemas"]["Fact_Annotated_int__FieldInfo_annotation_NoneType__required_True__metadata__Ge_ge_1800___Le_le_2100_____"];
            funds_destination?: components["schemas"]["Fact_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_1___MaxLen_max_length_2000_____"];
            objectives?: components["schemas"]["Fact_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_1___MaxLen_max_length_2000_____"];
            permitted_use?: components["schemas"]["Fact_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_1___MaxLen_max_length_2000_____"];
            region?: components["schemas"]["Fact_Region_"];
            sector?: components["schemas"]["Fact_Sector_"];
            shareholders?: components["schemas"]["Fact_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_1___MaxLen_max_length_2000_____"];
            source_url?: components["schemas"]["Fact_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_8___MaxLen_max_length_2000____PydanticGeneralMetadata_pattern__https_____"];
            stake_percent?: components["schemas"]["Fact_Annotated_Decimal__FieldInfo_annotation_NoneType__required_True__metadata__Ge_ge_0___Le_le_100____PydanticGeneralMetadata_decimal_places_2_____-Output"];
            tax_id?: components["schemas"]["Fact_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_3___MaxLen_max_length_30_____"];
            technology?: components["schemas"]["Fact_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_1___MaxLen_max_length_2000_____"];
        };
        /** CompanyResponse */
        CompanyResponse: {
            /** Alias */
            alias: string;
            /**
             * Created At
             * Format: date-time
             */
            created_at: string;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            profile: components["schemas"]["CompanyInput-Output"];
            /** Revision */
            revision: number;
            /**
             * Updated At
             * Format: date-time
             */
            updated_at: string;
        };
        /** CompanySummary */
        CompanySummary: {
            /** Alias */
            alias: string;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Name */
            name: string;
            /** Tax Id */
            tax_id: string | null;
            /**
             * Updated At
             * Format: date-time
             */
            updated_at: string;
        };
        /** CompanyUpdate */
        CompanyUpdate: {
            /** Expected Revision */
            expected_revision: number;
            profile: components["schemas"]["CompanyInput-Input"];
        };
        /**
         * DealType
         * @enum {string}
         */
        DealType: "PRIMARY" | "SECONDARY" | "MIXED";
        /** DocumentDetail */
        DocumentDetail: {
            /** Current Version */
            current_version: number;
            folder: components["schemas"]["Folder"];
            /**
             * Id
             * Format: uuid
             */
            id: string;
            latest: components["schemas"]["VersionResponse"];
            /**
             * Room Id
             * Format: uuid
             */
            room_id: string;
            /** Title */
            title: string;
            /** Versions */
            versions: components["schemas"]["VersionResponse"][];
        };
        /** DocumentResponse */
        DocumentResponse: {
            /** Current Version */
            current_version: number;
            folder: components["schemas"]["Folder"];
            /**
             * Id
             * Format: uuid
             */
            id: string;
            latest: components["schemas"]["VersionResponse"];
            /**
             * Room Id
             * Format: uuid
             */
            room_id: string;
            /** Title */
            title: string;
        };
        /** Fact[Annotated[Decimal, FieldInfo(annotation=NoneType, required=True, metadata=[Ge(ge=0), Le(le=100), _PydanticGeneralMetadata(decimal_places=2)])]] */
        "Fact_Annotated_Decimal__FieldInfo_annotation_NoneType__required_True__metadata__Ge_ge_0___Le_le_100____PydanticGeneralMetadata_decimal_places_2_____-Input": {
            /**
             * Entered By
             * @default
             */
            entered_by: string;
            /** @default NONE */
            issue: components["schemas"]["Issue"];
            /**
             * Notes
             * @default
             */
            notes: string;
            /**
             * Reviewed By
             * @default
             */
            reviewed_by: string;
            /** Reviewed On */
            reviewed_on?: string | null;
            /**
             * Source
             * @default
             */
            source: string;
            /** Source Date */
            source_date?: string | null;
            /** Value */
            value?: number | string | null;
            /** @default SELF_DECLARED */
            verification: components["schemas"]["Verification"];
        };
        /** Fact[Annotated[Decimal, FieldInfo(annotation=NoneType, required=True, metadata=[Ge(ge=0), Le(le=100), _PydanticGeneralMetadata(decimal_places=2)])]] */
        "Fact_Annotated_Decimal__FieldInfo_annotation_NoneType__required_True__metadata__Ge_ge_0___Le_le_100____PydanticGeneralMetadata_decimal_places_2_____-Output": {
            /**
             * Entered By
             * @default
             */
            entered_by: string;
            /** @default NONE */
            issue: components["schemas"]["Issue"];
            /**
             * Notes
             * @default
             */
            notes: string;
            /**
             * Reviewed By
             * @default
             */
            reviewed_by: string;
            /** Reviewed On */
            reviewed_on?: string | null;
            /**
             * Source
             * @default
             */
            source: string;
            /** Source Date */
            source_date?: string | null;
            /** Value */
            value?: string | null;
            /** @default SELF_DECLARED */
            verification: components["schemas"]["Verification"];
        };
        /** Fact[Annotated[Decimal, FieldInfo(annotation=NoneType, required=True, metadata=[Ge(ge=0), _PydanticGeneralMetadata(max_digits=18, decimal_places=2)])]] */
        "Fact_Annotated_Decimal__FieldInfo_annotation_NoneType__required_True__metadata__Ge_ge_0____PydanticGeneralMetadata_max_digits_18__decimal_places_2_____-Input": {
            /**
             * Entered By
             * @default
             */
            entered_by: string;
            /** @default NONE */
            issue: components["schemas"]["Issue"];
            /**
             * Notes
             * @default
             */
            notes: string;
            /**
             * Reviewed By
             * @default
             */
            reviewed_by: string;
            /** Reviewed On */
            reviewed_on?: string | null;
            /**
             * Source
             * @default
             */
            source: string;
            /** Source Date */
            source_date?: string | null;
            /** Value */
            value?: number | string | null;
            /** @default SELF_DECLARED */
            verification: components["schemas"]["Verification"];
        };
        /** Fact[Annotated[Decimal, FieldInfo(annotation=NoneType, required=True, metadata=[Ge(ge=0), _PydanticGeneralMetadata(max_digits=18, decimal_places=2)])]] */
        "Fact_Annotated_Decimal__FieldInfo_annotation_NoneType__required_True__metadata__Ge_ge_0____PydanticGeneralMetadata_max_digits_18__decimal_places_2_____-Output": {
            /**
             * Entered By
             * @default
             */
            entered_by: string;
            /** @default NONE */
            issue: components["schemas"]["Issue"];
            /**
             * Notes
             * @default
             */
            notes: string;
            /**
             * Reviewed By
             * @default
             */
            reviewed_by: string;
            /** Reviewed On */
            reviewed_on?: string | null;
            /**
             * Source
             * @default
             */
            source: string;
            /** Source Date */
            source_date?: string | null;
            /** Value */
            value?: string | null;
            /** @default SELF_DECLARED */
            verification: components["schemas"]["Verification"];
        };
        /** Fact[Annotated[Decimal, FieldInfo(annotation=NoneType, required=True, metadata=[_PydanticGeneralMetadata(max_digits=18, decimal_places=2)])]] */
        "Fact_Annotated_Decimal__FieldInfo_annotation_NoneType__required_True__metadata___PydanticGeneralMetadata_max_digits_18__decimal_places_2_____-Input": {
            /**
             * Entered By
             * @default
             */
            entered_by: string;
            /** @default NONE */
            issue: components["schemas"]["Issue"];
            /**
             * Notes
             * @default
             */
            notes: string;
            /**
             * Reviewed By
             * @default
             */
            reviewed_by: string;
            /** Reviewed On */
            reviewed_on?: string | null;
            /**
             * Source
             * @default
             */
            source: string;
            /** Source Date */
            source_date?: string | null;
            /** Value */
            value?: number | string | null;
            /** @default SELF_DECLARED */
            verification: components["schemas"]["Verification"];
        };
        /** Fact[Annotated[Decimal, FieldInfo(annotation=NoneType, required=True, metadata=[_PydanticGeneralMetadata(max_digits=18, decimal_places=2)])]] */
        "Fact_Annotated_Decimal__FieldInfo_annotation_NoneType__required_True__metadata___PydanticGeneralMetadata_max_digits_18__decimal_places_2_____-Output": {
            /**
             * Entered By
             * @default
             */
            entered_by: string;
            /** @default NONE */
            issue: components["schemas"]["Issue"];
            /**
             * Notes
             * @default
             */
            notes: string;
            /**
             * Reviewed By
             * @default
             */
            reviewed_by: string;
            /** Reviewed On */
            reviewed_on?: string | null;
            /**
             * Source
             * @default
             */
            source: string;
            /** Source Date */
            source_date?: string | null;
            /** Value */
            value?: string | null;
            /** @default SELF_DECLARED */
            verification: components["schemas"]["Verification"];
        };
        /** Fact[Annotated[int, FieldInfo(annotation=NoneType, required=True, metadata=[Ge(ge=0), Le(le=10000000)])]] */
        Fact_Annotated_int__FieldInfo_annotation_NoneType__required_True__metadata__Ge_ge_0___Le_le_10000000_____: {
            /**
             * Entered By
             * @default
             */
            entered_by: string;
            /** @default NONE */
            issue: components["schemas"]["Issue"];
            /**
             * Notes
             * @default
             */
            notes: string;
            /**
             * Reviewed By
             * @default
             */
            reviewed_by: string;
            /** Reviewed On */
            reviewed_on?: string | null;
            /**
             * Source
             * @default
             */
            source: string;
            /** Source Date */
            source_date?: string | null;
            /** Value */
            value?: number | null;
            /** @default SELF_DECLARED */
            verification: components["schemas"]["Verification"];
        };
        /** Fact[Annotated[int, FieldInfo(annotation=NoneType, required=True, metadata=[Ge(ge=1800), Le(le=2100)])]] */
        Fact_Annotated_int__FieldInfo_annotation_NoneType__required_True__metadata__Ge_ge_1800___Le_le_2100_____: {
            /**
             * Entered By
             * @default
             */
            entered_by: string;
            /** @default NONE */
            issue: components["schemas"]["Issue"];
            /**
             * Notes
             * @default
             */
            notes: string;
            /**
             * Reviewed By
             * @default
             */
            reviewed_by: string;
            /** Reviewed On */
            reviewed_on?: string | null;
            /**
             * Source
             * @default
             */
            source: string;
            /** Source Date */
            source_date?: string | null;
            /** Value */
            value?: number | null;
            /** @default SELF_DECLARED */
            verification: components["schemas"]["Verification"];
        };
        /** Fact[Annotated[str, FieldInfo(annotation=NoneType, required=True, metadata=[MinLen(min_length=1), MaxLen(max_length=2000)])]] */
        Fact_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_1___MaxLen_max_length_2000_____: {
            /**
             * Entered By
             * @default
             */
            entered_by: string;
            /** @default NONE */
            issue: components["schemas"]["Issue"];
            /**
             * Notes
             * @default
             */
            notes: string;
            /**
             * Reviewed By
             * @default
             */
            reviewed_by: string;
            /** Reviewed On */
            reviewed_on?: string | null;
            /**
             * Source
             * @default
             */
            source: string;
            /** Source Date */
            source_date?: string | null;
            /** Value */
            value?: string | null;
            /** @default SELF_DECLARED */
            verification: components["schemas"]["Verification"];
        };
        /** Fact[Annotated[str, FieldInfo(annotation=NoneType, required=True, metadata=[MinLen(min_length=1), MaxLen(max_length=200)])]] */
        Fact_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_1___MaxLen_max_length_200_____: {
            /**
             * Entered By
             * @default
             */
            entered_by: string;
            /** @default NONE */
            issue: components["schemas"]["Issue"];
            /**
             * Notes
             * @default
             */
            notes: string;
            /**
             * Reviewed By
             * @default
             */
            reviewed_by: string;
            /** Reviewed On */
            reviewed_on?: string | null;
            /**
             * Source
             * @default
             */
            source: string;
            /** Source Date */
            source_date?: string | null;
            /** Value */
            value?: string | null;
            /** @default SELF_DECLARED */
            verification: components["schemas"]["Verification"];
        };
        /** Fact[Annotated[str, FieldInfo(annotation=NoneType, required=True, metadata=[MinLen(min_length=3), MaxLen(max_length=30)])]] */
        Fact_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_3___MaxLen_max_length_30_____: {
            /**
             * Entered By
             * @default
             */
            entered_by: string;
            /** @default NONE */
            issue: components["schemas"]["Issue"];
            /**
             * Notes
             * @default
             */
            notes: string;
            /**
             * Reviewed By
             * @default
             */
            reviewed_by: string;
            /** Reviewed On */
            reviewed_on?: string | null;
            /**
             * Source
             * @default
             */
            source: string;
            /** Source Date */
            source_date?: string | null;
            /** Value */
            value?: string | null;
            /** @default SELF_DECLARED */
            verification: components["schemas"]["Verification"];
        };
        /** Fact[Annotated[str, FieldInfo(annotation=NoneType, required=True, metadata=[MinLen(min_length=8), MaxLen(max_length=2000), _PydanticGeneralMetadata(pattern='https?://\\S+')])]] */
        Fact_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_8___MaxLen_max_length_2000____PydanticGeneralMetadata_pattern__https_____: {
            /**
             * Entered By
             * @default
             */
            entered_by: string;
            /** @default NONE */
            issue: components["schemas"]["Issue"];
            /**
             * Notes
             * @default
             */
            notes: string;
            /**
             * Reviewed By
             * @default
             */
            reviewed_by: string;
            /** Reviewed On */
            reviewed_on?: string | null;
            /**
             * Source
             * @default
             */
            source: string;
            /** Source Date */
            source_date?: string | null;
            /** Value */
            value?: string | null;
            /** @default SELF_DECLARED */
            verification: components["schemas"]["Verification"];
        };
        /** Fact[DealType] */
        Fact_DealType_: {
            /**
             * Entered By
             * @default
             */
            entered_by: string;
            /** @default NONE */
            issue: components["schemas"]["Issue"];
            /**
             * Notes
             * @default
             */
            notes: string;
            /**
             * Reviewed By
             * @default
             */
            reviewed_by: string;
            /** Reviewed On */
            reviewed_on?: string | null;
            /**
             * Source
             * @default
             */
            source: string;
            /** Source Date */
            source_date?: string | null;
            value?: components["schemas"]["DealType"] | null;
            /** @default SELF_DECLARED */
            verification: components["schemas"]["Verification"];
        };
        /** Fact[Region] */
        Fact_Region_: {
            /**
             * Entered By
             * @default
             */
            entered_by: string;
            /** @default NONE */
            issue: components["schemas"]["Issue"];
            /**
             * Notes
             * @default
             */
            notes: string;
            /**
             * Reviewed By
             * @default
             */
            reviewed_by: string;
            /** Reviewed On */
            reviewed_on?: string | null;
            /**
             * Source
             * @default
             */
            source: string;
            /** Source Date */
            source_date?: string | null;
            value?: components["schemas"]["Region"] | null;
            /** @default SELF_DECLARED */
            verification: components["schemas"]["Verification"];
        };
        /** Fact[Sector] */
        Fact_Sector_: {
            /**
             * Entered By
             * @default
             */
            entered_by: string;
            /** @default NONE */
            issue: components["schemas"]["Issue"];
            /**
             * Notes
             * @default
             */
            notes: string;
            /**
             * Reviewed By
             * @default
             */
            reviewed_by: string;
            /** Reviewed On */
            reviewed_on?: string | null;
            /**
             * Source
             * @default
             */
            source: string;
            /** Source Date */
            source_date?: string | null;
            value?: components["schemas"]["Sector"] | null;
            /** @default SELF_DECLARED */
            verification: components["schemas"]["Verification"];
        };
        /** Fact[Union[Annotated[str, FieldInfo(annotation=NoneType, required=True, metadata=[MinLen(min_length=1), MaxLen(max_length=2000)])], Decimal, int]] */
        Fact_Union_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_1___MaxLen_max_length_2000______Decimal__int__: {
            /**
             * Entered By
             * @default
             */
            entered_by: string;
            /** @default NONE */
            issue: components["schemas"]["Issue"];
            /**
             * Notes
             * @default
             */
            notes: string;
            /**
             * Reviewed By
             * @default
             */
            reviewed_by: string;
            /** Reviewed On */
            reviewed_on?: string | null;
            /**
             * Source
             * @default
             */
            source: string;
            /** Source Date */
            source_date?: string | null;
            /** Value */
            value?: string | number | null;
            /** @default SELF_DECLARED */
            verification: components["schemas"]["Verification"];
        };
        /** FinancialYear */
        "FinancialYear-Input": {
            ebitda_vnd?: components["schemas"]["Fact_Annotated_Decimal__FieldInfo_annotation_NoneType__required_True__metadata___PydanticGeneralMetadata_max_digits_18__decimal_places_2_____-Input"];
            revenue_vnd?: components["schemas"]["Fact_Annotated_Decimal__FieldInfo_annotation_NoneType__required_True__metadata__Ge_ge_0____PydanticGeneralMetadata_max_digits_18__decimal_places_2_____-Input"];
            /** Year */
            year: number;
        };
        /** FinancialYear */
        "FinancialYear-Output": {
            ebitda_vnd?: components["schemas"]["Fact_Annotated_Decimal__FieldInfo_annotation_NoneType__required_True__metadata___PydanticGeneralMetadata_max_digits_18__decimal_places_2_____-Output"];
            revenue_vnd?: components["schemas"]["Fact_Annotated_Decimal__FieldInfo_annotation_NoneType__required_True__metadata__Ge_ge_0____PydanticGeneralMetadata_max_digits_18__decimal_places_2_____-Output"];
            /** Year */
            year: number;
        };
        /**
         * Folder
         * @enum {string}
         */
        Folder: "LEGAL_CORPORATE" | "FINANCIAL_TAX" | "COMMERCIAL_OPERATIONS" | "TECHNOLOGY_IP" | "HUMAN_RESOURCES" | "QA_TRACKER";
        /** FolderResponse */
        FolderResponse: {
            /** Document Count */
            document_count: number;
            id: components["schemas"]["Folder"];
            /** Label */
            label: string;
        };
        /** HTTPValidationError */
        HTTPValidationError: {
            /** Detail */
            detail?: components["schemas"]["ValidationError"][];
        };
        /** HealthResponse */
        HealthResponse: {
            /**
             * Scope
             * @constant
             */
            scope: "liveness";
            /** Service */
            service: string;
            /**
             * Status
             * @constant
             */
            status: "ok";
            /** Version */
            version: string;
        };
        /** IdentifiedPreview */
        IdentifiedPreview: {
            /** Facts */
            facts: {
                [key: string]: components["schemas"]["Fact_Union_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_1___MaxLen_max_length_2000______Decimal__int__"];
            };
            /** Financials */
            financials: components["schemas"]["FinancialYear-Output"][];
            /**
             * Layer
             * @default 2
             */
            layer: number;
            /**
             * Notice
             * @default Bản xem trước nội bộ; không phải quyền chia sẻ cho buyer.
             */
            notice: string;
        };
        /**
         * Issue
         * @enum {string}
         */
        Issue: "NONE" | "CONFLICTED" | "EXPIRED";
        /**
         * Region
         * @enum {string}
         */
        Region: "NORTH" | "CENTRAL" | "SOUTH";
        /** RestrictedPreview */
        RestrictedPreview: {
            /** Facts */
            facts: {
                [key: string]: components["schemas"]["Fact_Annotated_str__FieldInfo_annotation_NoneType__required_True__metadata__MinLen_min_length_1___MaxLen_max_length_2000_____"];
            };
            /**
             * Layer
             * @default 3
             */
            layer: number;
            /**
             * Notice
             * @default Nội dung hạn chế và phòng dữ liệu; chưa triển khai NDA/phê duyệt hay quyền buyer.
             */
            notice: string;
        };
        /** RoomDetail */
        RoomDetail: {
            /** Allowed Extensions */
            allowed_extensions: string[];
            /**
             * Company Id
             * Format: uuid
             */
            company_id: string;
            /** Company Name */
            company_name: string;
            /**
             * Created At
             * Format: date-time
             */
            created_at: string;
            /** Documents */
            documents: components["schemas"]["DocumentResponse"][];
            /** Folders */
            folders: components["schemas"]["FolderResponse"][];
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Max Upload Bytes */
            max_upload_bytes: number;
            /** Title */
            title: string;
        };
        /** RoomInput */
        RoomInput: {
            /**
             * Company Id
             * Format: uuid
             */
            company_id: string;
            /** Title */
            title: string;
        };
        /** RoomResponse */
        RoomResponse: {
            /**
             * Company Id
             * Format: uuid
             */
            company_id: string;
            /** Company Name */
            company_name: string;
            /**
             * Created At
             * Format: date-time
             */
            created_at: string;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Title */
            title: string;
        };
        /**
         * Sector
         * @enum {string}
         */
        Sector: "SOFTWARE" | "MANUFACTURING" | "SERVICES" | "OTHER";
        /** ValidationError */
        ValidationError: {
            /** Context */
            ctx?: Record<string, never>;
            /** Input */
            input?: unknown;
            /** Location */
            loc: (string | number)[];
            /** Message */
            msg: string;
            /** Error Type */
            type: string;
        };
        /**
         * Verification
         * @enum {string}
         */
        Verification: "SELF_DECLARED" | "DOCUMENT_VERIFIED" | "THIRD_PARTY_CONFIRMED";
        /** VersionResponse */
        VersionResponse: {
            /** Filename */
            filename: string;
            /** Media Type */
            media_type: string;
            /** Note */
            note: string;
            /** Number */
            number: number;
            /** Sha256 */
            sha256: string;
            /** Size Bytes */
            size_bytes: number;
            /**
             * Uploaded At
             * Format: date-time
             */
            uploaded_at: string;
        };
    };
    responses: never;
    parameters: never;
    requestBodies: never;
    headers: never;
    pathItems: never;
}
export type $defs = Record<string, never>;
export interface operations {
    list_companies: {
        parameters: {
            query?: {
                q?: string;
                offset?: number;
                limit?: number;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["CompanySummary"][];
                };
            };
            /** @description Forbidden */
            403: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Not Found */
            404: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Conflict */
            409: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
            /** @description Service Unavailable */
            503: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
        };
    };
    create_company: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["CompanyInput-Input"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["CompanyResponse"];
                };
            };
            /** @description Forbidden */
            403: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Not Found */
            404: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Conflict */
            409: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
            /** @description Service Unavailable */
            503: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
        };
    };
    get_company: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                company_id: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["CompanyResponse"];
                };
            };
            /** @description Forbidden */
            403: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Not Found */
            404: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Conflict */
            409: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
            /** @description Service Unavailable */
            503: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
        };
    };
    update_company: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                company_id: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["CompanyUpdate"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["CompanyResponse"];
                };
            };
            /** @description Forbidden */
            403: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Not Found */
            404: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Conflict */
            409: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
            /** @description Service Unavailable */
            503: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
        };
    };
    preview_company: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                company_id: string;
                layer: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["AnonymousPreview"] | components["schemas"]["IdentifiedPreview"] | components["schemas"]["RestrictedPreview"];
                };
            };
            /** @description Forbidden */
            403: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Not Found */
            404: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Conflict */
            409: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
            /** @description Service Unavailable */
            503: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
        };
    };
    get_health: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HealthResponse"];
                };
            };
        };
    };
    list_rooms: {
        parameters: {
            query?: {
                company_id?: string | null;
                offset?: number;
                limit?: number;
            };
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["RoomResponse"][];
                };
            };
            /** @description Forbidden */
            403: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Not Found */
            404: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Conflict */
            409: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Content Too Large */
            413: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Unsupported Media Type */
            415: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
            /** @description Service Unavailable */
            503: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
        };
    };
    create_room: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["RoomInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["RoomResponse"];
                };
            };
            /** @description Forbidden */
            403: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Not Found */
            404: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Conflict */
            409: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Content Too Large */
            413: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Unsupported Media Type */
            415: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
            /** @description Service Unavailable */
            503: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
        };
    };
    get_room: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                room_id: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["RoomDetail"];
                };
            };
            /** @description Forbidden */
            403: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Not Found */
            404: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Conflict */
            409: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Content Too Large */
            413: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Unsupported Media Type */
            415: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
            /** @description Service Unavailable */
            503: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
        };
    };
    upload_document: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                room_id: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "multipart/form-data": components["schemas"]["Body_upload_document"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["DocumentDetail"];
                };
            };
            /** @description Forbidden */
            403: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Not Found */
            404: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Conflict */
            409: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Content Too Large */
            413: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Unsupported Media Type */
            415: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
            /** @description Service Unavailable */
            503: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
        };
    };
    get_document: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                room_id: string;
                document_id: string;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["DocumentDetail"];
                };
            };
            /** @description Forbidden */
            403: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Not Found */
            404: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Conflict */
            409: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Content Too Large */
            413: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Unsupported Media Type */
            415: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
            /** @description Service Unavailable */
            503: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
        };
    };
    upload_version: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                room_id: string;
                document_id: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "multipart/form-data": components["schemas"]["Body_upload_version"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["DocumentDetail"];
                };
            };
            /** @description Forbidden */
            403: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Not Found */
            404: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Conflict */
            409: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Content Too Large */
            413: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Unsupported Media Type */
            415: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
            /** @description Service Unavailable */
            503: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
        };
    };
    get_document_content: {
        parameters: {
            query?: {
                download?: boolean;
            };
            header?: never;
            path: {
                room_id: string;
                document_id: string;
                number: number;
            };
            cookie?: never;
        };
        requestBody?: never;
        responses: {
            /** @description Immutable version bytes; Office files are attachment-only. */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/pdf": string;
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": string;
                    "application/vnd.openxmlformats-officedocument.wordprocessingml.document": string;
                    "image/jpeg": string;
                    "image/png": string;
                    "text/plain": string;
                };
            };
            /** @description Forbidden */
            403: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Not Found */
            404: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Conflict */
            409: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Content Too Large */
            413: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Unsupported Media Type */
            415: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
            /** @description Validation Error */
            422: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["HTTPValidationError"];
                };
            };
            /** @description Service Unavailable */
            503: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ApiError"];
                };
            };
        };
    };
}
