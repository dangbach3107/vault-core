// Generated from contracts/openapi.json. Do not edit.
export interface paths {
    "/api/v1/auth/login": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Login */
        post: operations["login"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/auth/me": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Me */
        get: operations["current_session"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
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
        /** Delete Company */
        delete: operations["delete_company"];
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
    "/api/v1/companies/{company_id}/reviews": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** List Company Reviews */
        get: operations["list_company_reviews"];
        put?: never;
        /** Request Review */
        post: operations["request_fact_review"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/deals": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** List Deals */
        get: operations["list_deals"];
        put?: never;
        /** Create Deal */
        post: operations["create_deal"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/deals/catalog": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get Catalog */
        get: operations["get_deal_catalog"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/deals/{deal_id}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get Deal */
        get: operations["get_deal"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/deals/{deal_id}/access-grants/{grant_id}/revoke": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Revoke Deal Access */
        post: operations["revoke_deal_access"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/deals/{deal_id}/access-requests": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Request Deal Access */
        post: operations["request_deal_access"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/deals/{deal_id}/access-requests/{request_id}/decision": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Decide Deal Access */
        post: operations["decide_deal_access"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/deals/{deal_id}/actions/{action}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Complete Action */
        post: operations["complete_deal_action"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/deals/{deal_id}/closing-evidence": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** List Closing Evidence */
        get: operations["list_closing_evidence"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/deals/{deal_id}/closing-evidence/{document_id}/content": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get Closing Evidence Content */
        get: operations["get_closing_evidence_content"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/deals/{deal_id}/complete-sample": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Complete Sample */
        post: operations["complete_sample_deal"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/deals/{deal_id}/documents": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * List Deal Documents
         * @description Files the current buyer may open: exactly the version that was approved.
         */
        get: operations["list_deal_documents"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/deals/{deal_id}/documents/{grant_id}/{document_id}/content": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get Deal Document Content */
        get: operations["get_deal_document_content"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/deals/{deal_id}/fees": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Add Fee */
        post: operations["add_deal_fee"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/deals/{deal_id}/fees/{fee_id}/invoice": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Issue Invoice */
        post: operations["issue_fee_invoice"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/deals/{deal_id}/fees/{fee_id}/payments": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Record Payment */
        post: operations["record_fee_payment"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/deals/{deal_id}/profile/{layer}": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** Get Deal Profile */
        get: operations["get_deal_profile"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/deals/{deal_id}/reset": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Reset Deal */
        post: operations["reset_deal"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/deals/{deal_id}/teaser": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /**
         * Get Deal Teaser
         * @description Layer 1 for the deal's buyer, only after the seller approved the teaser.
         */
        get: operations["get_deal_teaser"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/deals/{deal_id}/tech-dd/findings": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Add Finding */
        post: operations["add_tech_dd_finding"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/deals/{deal_id}/tech-dd/findings/{finding_id}/status": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Update Finding */
        post: operations["update_tech_dd_finding"];
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/deals/{deal_id}/workflow/{step}/complete": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Complete Workflow Step */
        post: operations["complete_workflow_step"];
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
    "/api/v1/reviews": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        /** List Reviews */
        get: operations["list_reviews"];
        put?: never;
        post?: never;
        delete?: never;
        options?: never;
        head?: never;
        patch?: never;
        trace?: never;
    };
    "/api/v1/reviews/{review_id}/decision": {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        get?: never;
        put?: never;
        /** Decide Review */
        post: operations["decide_fact_review"];
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
        /** Delete Room */
        delete: operations["delete_room"];
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
        /** Delete Document */
        delete: operations["delete_document"];
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
        /** AccessDecisionInput */
        AccessDecisionInput: {
            /** Approved */
            approved: boolean;
            /**
             * Basis Ref
             * @default
             */
            basis_ref: string;
            /**
             * Can Download
             * @default false
             */
            can_download: boolean;
            /** Document Ids */
            document_ids?: string[] | null;
            /** Expires At */
            expires_at?: string | null;
            /** Reason */
            reason: string;
        };
        /** AccessRequestInput */
        AccessRequestInput: {
            /** Document Ids */
            document_ids?: string[];
            /** Purpose */
            purpose: string;
            /**
             * Requested Level
             * @enum {string}
             */
            requested_level: "L0" | "L1" | "L2" | "L3" | "CLOSING";
        };
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
        /** BuyerRequestForm */
        BuyerRequestForm: {
            /** Budget Max Vnd */
            budget_max_vnd?: number | string | null;
            /** Budget Min Vnd */
            budget_min_vnd?: number | string | null;
            /** Capability */
            capability: string;
            /**
             * Goal
             * @default
             */
            goal: string;
            /**
             * Timeline
             * @default
             */
            timeline: string;
        };
        /** CatalogAction */
        CatalogAction: {
            /**
             * Key
             * @enum {string}
             */
            key: "buyerRequest" | "sellerProfile" | "prepPackageFeeRecorded" | "sellerL1Approval" | "matchPrepared" | "identityRequested" | "ndaRecorded" | "sellerL2Approval" | "indicativeLoiSubmitted" | "legalL3Approval" | "crossBorderApproval" | "noEscrowConfirmed" | "sellerFileApproval" | "vdrOpened" | "techDdSigned" | "loiSubmitted" | "legalClosingChecklist" | "spaSigned" | "dealClosed" | "successFeeRecorded" | "postDealHandoff";
            /** Label */
            label: string;
            /** Requires */
            requires: string[];
            /** Role */
            role: string;
        };
        /** CatalogStage */
        CatalogStage: {
            /** Label */
            label: string;
            /** Number */
            number: number;
            /** Owner */
            owner: string;
        };
        /** ClosingEvidence */
        ClosingEvidence: {
            /** Action */
            action: string;
            /** Action Label */
            action_label: string;
            /**
             * Document Id
             * Format: uuid
             */
            document_id: string;
            /** Filename */
            filename: string;
            /** Media Type */
            media_type: string;
            /** Title */
            title: string;
            /** Version Number */
            version_number: number;
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
            /** Owner Username */
            owner_username: string;
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
            deal_type?: components["schemas"]["DealType"] | null;
            /** Employee Band */
            employee_band?: string | null;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Name */
            name: string;
            /** Owner Username */
            owner_username: string;
            region?: components["schemas"]["Region"] | null;
            /** Revenue Band */
            revenue_band?: string | null;
            sector?: components["schemas"]["Sector"] | null;
            /** Stake Percent */
            stake_percent?: string | null;
            /** Tax Id */
            tax_id: string | null;
            /**
             * Total Facts Count
             * @default 0
             */
            total_facts_count: number;
            /**
             * Updated At
             * Format: date-time
             */
            updated_at: string;
            /**
             * Verified Facts Count
             * @default 0
             */
            verified_facts_count: number;
        };
        /** CompanyUpdate */
        CompanyUpdate: {
            /** Expected Revision */
            expected_revision: number;
            profile: components["schemas"]["CompanyInput-Input"];
        };
        /** DealActionInput */
        DealActionInput: {
            buyer_request?: components["schemas"]["BuyerRequestForm"] | null;
            /** Document Ids */
            document_ids?: string[];
            handoff?: components["schemas"]["HandoffForm"] | null;
            nda?: components["schemas"]["NdaForm"] | null;
            /**
             * Note
             * @default
             */
            note: string;
            offer?: components["schemas"]["OfferForm"] | null;
        };
        /** DealCatalog */
        DealCatalog: {
            /** Actions */
            actions: components["schemas"]["CatalogAction"][];
            /** Buyers */
            buyers: string[];
            /** Stages */
            stages: components["schemas"]["CatalogStage"][];
        };
        /** DealCreate */
        DealCreate: {
            /** Buyer Username */
            buyer_username?: string | null;
            /** Seller Company Id */
            seller_company_id?: string | null;
            /**
             * Title
             * @default Japanese buyer × Vietnamese warehouse software seller
             */
            title: string;
        };
        /** DealDocument */
        DealDocument: {
            /** Can Download */
            can_download: boolean;
            /**
             * Document Id
             * Format: uuid
             */
            document_id: string;
            /**
             * Expires At
             * Format: date-time
             */
            expires_at: string;
            /** Filename */
            filename: string;
            /**
             * Grant Id
             * Format: uuid
             */
            grant_id: string;
            /** Latest Version */
            latest_version: number;
            /** Media Type */
            media_type: string;
            /** Title */
            title: string;
            /** Version Number */
            version_number: number;
        };
        /** DealResponse */
        DealResponse: {
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
            /** Revision */
            revision: number;
            /** State */
            state: {
                [key: string]: unknown;
            };
            /** Title */
            title: string;
            /**
             * Updated At
             * Format: date-time
             */
            updated_at: string;
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
        /** FeeInput */
        FeeInput: {
            /** Amount Vnd */
            amount_vnd: number | string;
            /**
             * Due On
             * Format: date
             */
            due_on: string;
            /**
             * Note
             * @default
             */
            note: string;
            /**
             * Type
             * @enum {string}
             */
            type: "PREP_PACKAGE" | "TECH_DD" | "SUCCESS_FEE";
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
        /** FindingInput */
        FindingInput: {
            /**
             * Description
             * @default
             */
            description: string;
            /** Impact Vnd */
            impact_vnd?: number | string | null;
            /**
             * Remediation
             * @default
             */
            remediation: string;
            /**
             * Severity
             * @enum {string}
             */
            severity: "LOW" | "MEDIUM" | "HIGH" | "CRITICAL";
            /** Title */
            title: string;
        };
        /** FindingUpdate */
        FindingUpdate: {
            /** Note */
            note: string;
            /**
             * Status
             * @enum {string}
             */
            status: "OPEN" | "RESPONDED" | "RESOLVED" | "ACCEPTED_RISK";
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
        /** HandoffForm */
        HandoffForm: {
            /**
             * Handed On
             * Format: date
             */
            handed_on: string;
            /** Items */
            items: string[];
            /** Recipient */
            recipient: string;
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
        /** InvoiceInput */
        InvoiceInput: {
            /** Invoice Number */
            invoice_number: string;
            /**
             * Issued On
             * Format: date
             */
            issued_on: string;
        };
        /**
         * Issue
         * @enum {string}
         */
        Issue: "NONE" | "CONFLICTED" | "EXPIRED";
        /** LoginInput */
        LoginInput: {
            /** Password */
            password: string;
            /** Username */
            username: string;
        };
        /** LoginResponse */
        LoginResponse: {
            /** Access Token */
            access_token: string;
            /**
             * Token Type
             * @default bearer
             */
            token_type: string;
            user: components["schemas"]["UserResponse"];
        };
        /** NdaForm */
        NdaForm: {
            /** Document Id */
            document_id?: string | null;
            /**
             * Expires On
             * Format: date
             */
            expires_on: string;
            /** Parties */
            parties: string[];
            /** Reference */
            reference: string;
            /**
             * Signed On
             * Format: date
             */
            signed_on: string;
        };
        /**
         * OfferForm
         * @description LOI sơ bộ (không ràng buộc) hoặc đề nghị chính thức.
         */
        OfferForm: {
            /**
             * Conditions
             * @default
             */
            conditions: string;
            /**
             * Exclusivity Days
             * @default 0
             */
            exclusivity_days: number;
            /** Price High Vnd */
            price_high_vnd?: number | string | null;
            /** Price Low Vnd */
            price_low_vnd: number | string;
            /** Reference */
            reference: string;
            /**
             * Valid Until
             * Format: date
             */
            valid_until: string;
            /**
             * Valuation Basis
             * @enum {string}
             */
            valuation_basis: "EV" | "EQUITY";
        };
        /** PaymentInput */
        PaymentInput: {
            /** Amount Vnd */
            amount_vnd: number | string;
            /**
             * Paid On
             * Format: date
             */
            paid_on: string;
            /** Reference */
            reference: string;
        };
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
        /** ReviewDecisionInput */
        ReviewDecisionInput: {
            /** Approved */
            approved: boolean;
            /** Reason */
            reason: string;
            /** Verification */
            verification?: ("DOCUMENT_VERIFIED" | "THIRD_PARTY_CONFIRMED") | null;
        };
        /** ReviewDocument */
        ReviewDocument: {
            /**
             * Document Id
             * Format: uuid
             */
            document_id: string;
            /** Filename */
            filename: string;
            /**
             * Room Id
             * Format: uuid
             */
            room_id: string;
            /** Title */
            title: string;
            /** Version Number */
            version_number: number;
        };
        /** ReviewRequestInput */
        ReviewRequestInput: {
            /** Document Id */
            document_id?: string | null;
            /** Field */
            field: string;
            /**
             * Note
             * @default
             */
            note: string;
            /** Source */
            source: string;
            /**
             * Source Date
             * Format: date
             */
            source_date: string;
        };
        /** ReviewResponse */
        ReviewResponse: {
            /** Company Alias */
            company_alias: string;
            /**
             * Company Id
             * Format: uuid
             */
            company_id: string;
            /** Company Name */
            company_name: string;
            /** Decided At */
            decided_at: string | null;
            /** Decided By */
            decided_by: string | null;
            document: components["schemas"]["ReviewDocument"] | null;
            /** Field */
            field: string;
            /**
             * Id
             * Format: uuid
             */
            id: string;
            /** Note */
            note: string;
            /** Reason */
            reason: string;
            /**
             * Requested At
             * Format: date-time
             */
            requested_at: string;
            /** Requested By */
            requested_by: string;
            /** Source */
            source: string;
            /**
             * Source Date
             * Format: date
             */
            source_date: string;
            /**
             * Status
             * @enum {string}
             */
            status: "PENDING" | "APPROVED" | "REJECTED";
            /** Value */
            value: unknown;
            /** Verification */
            verification: string | null;
        };
        /** RevokeAccessInput */
        RevokeAccessInput: {
            /** Reason */
            reason: string;
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
        /** UserResponse */
        UserResponse: {
            /** Display Name */
            display_name: string;
            /**
             * Role
             * @enum {string}
             */
            role: "BUYER" | "SELLER" | "VAULT_ADMIN" | "LEGAL" | "TECH_DD" | "FINANCE";
            /** Username */
            username: string;
        };
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
        /** WorkflowStepInput */
        WorkflowStepInput: {
            /** Note */
            note: string;
            /** Opened Data */
            opened_data?: string[];
            /**
             * Outcome
             * @default CONTINUE
             * @enum {string}
             */
            outcome: "CONTINUE" | "STOP";
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
    login: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["LoginInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["LoginResponse"];
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
            /** @description Too many failed attempts. */
            429: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
            };
        };
    };
    current_session: {
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
                    "application/json": components["schemas"]["UserResponse"];
                };
            };
        };
    };
    list_companies: {
        parameters: {
            query?: {
                q?: string;
                sector?: components["schemas"]["Sector"] | null;
                region?: components["schemas"]["Region"] | null;
                deal_type?: components["schemas"]["DealType"] | null;
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
    delete_company: {
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
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
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
    list_company_reviews: {
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
                    "application/json": components["schemas"]["ReviewResponse"][];
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
    request_fact_review: {
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
                "application/json": components["schemas"]["ReviewRequestInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ReviewResponse"];
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
    list_deals: {
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
                    "application/json": components["schemas"]["DealResponse"][];
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
    create_deal: {
        parameters: {
            query?: never;
            header?: never;
            path?: never;
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["DealCreate"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["DealResponse"];
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
    get_deal_catalog: {
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
                    "application/json": components["schemas"]["DealCatalog"];
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
    get_deal: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                deal_id: string;
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
                    "application/json": components["schemas"]["DealResponse"];
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
    revoke_deal_access: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                deal_id: string;
                grant_id: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["RevokeAccessInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["DealResponse"];
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
    request_deal_access: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                deal_id: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["AccessRequestInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["DealResponse"];
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
    decide_deal_access: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                deal_id: string;
                request_id: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["AccessDecisionInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["DealResponse"];
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
    complete_deal_action: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                deal_id: string;
                action: "buyerRequest" | "sellerProfile" | "prepPackageFeeRecorded" | "sellerL1Approval" | "matchPrepared" | "identityRequested" | "ndaRecorded" | "sellerL2Approval" | "indicativeLoiSubmitted" | "legalL3Approval" | "crossBorderApproval" | "noEscrowConfirmed" | "sellerFileApproval" | "vdrOpened" | "techDdSigned" | "loiSubmitted" | "legalClosingChecklist" | "spaSigned" | "dealClosed" | "successFeeRecorded" | "postDealHandoff";
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["DealActionInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["DealResponse"];
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
    list_closing_evidence: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                deal_id: string;
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
                    "application/json": components["schemas"]["ClosingEvidence"][];
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
    get_closing_evidence_content: {
        parameters: {
            query?: {
                download?: boolean;
            };
            header?: never;
            path: {
                deal_id: string;
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
                content?: never;
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
    complete_sample_deal: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                deal_id: string;
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
                    "application/json": components["schemas"]["DealResponse"];
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
    list_deal_documents: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                deal_id: string;
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
                    "application/json": components["schemas"]["DealDocument"][];
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
    get_deal_document_content: {
        parameters: {
            query?: {
                download?: boolean;
            };
            header?: never;
            path: {
                deal_id: string;
                grant_id: string;
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
                content?: never;
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
    add_deal_fee: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                deal_id: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["FeeInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["DealResponse"];
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
    issue_fee_invoice: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                deal_id: string;
                fee_id: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["InvoiceInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["DealResponse"];
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
    record_fee_payment: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                deal_id: string;
                fee_id: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["PaymentInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["DealResponse"];
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
    get_deal_profile: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                deal_id: string;
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
                    "application/json": components["schemas"]["IdentifiedPreview"] | components["schemas"]["RestrictedPreview"];
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
    reset_deal: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                deal_id: string;
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
                    "application/json": components["schemas"]["DealResponse"];
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
    get_deal_teaser: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                deal_id: string;
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
                    "application/json": components["schemas"]["AnonymousPreview"];
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
    add_tech_dd_finding: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                deal_id: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["FindingInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            201: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["DealResponse"];
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
    update_tech_dd_finding: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                deal_id: string;
                finding_id: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["FindingUpdate"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["DealResponse"];
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
    complete_workflow_step: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                deal_id: string;
                step: number;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["WorkflowStepInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["DealResponse"];
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
    list_reviews: {
        parameters: {
            query?: {
                status?: ("PENDING" | "APPROVED" | "REJECTED") | null;
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
                    "application/json": components["schemas"]["ReviewResponse"][];
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
    decide_fact_review: {
        parameters: {
            query?: never;
            header?: never;
            path: {
                review_id: string;
            };
            cookie?: never;
        };
        requestBody: {
            content: {
                "application/json": components["schemas"]["ReviewDecisionInput"];
            };
        };
        responses: {
            /** @description Successful Response */
            200: {
                headers: {
                    [name: string]: unknown;
                };
                content: {
                    "application/json": components["schemas"]["ReviewResponse"];
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
    delete_room: {
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
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
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
    delete_document: {
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
            204: {
                headers: {
                    [name: string]: unknown;
                };
                content?: never;
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
