-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Erstellungszeit: 03. Feb 2022 um 12:53
-- Server-Version: 10.4.22-MariaDB
-- PHP-Version: 8.1.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Datenbank: `powermap`
--

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `balancing_areas`
--

CREATE TABLE `balancing_areas` (
  `id` int(11) NOT NULL,
  `yeic` varchar(50) DEFAULT NULL,
  `balancing_area_grid_connection_point` varchar(500) DEFAULT NULL,
  `control_area_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `catalog`
--

CREATE TABLE `catalog` (
  `id` int(11) NOT NULL,
  `category_id` int(11) NOT NULL,
  `name_DE` varchar(500) NOT NULL,
  `name_EN` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `catalog_categories`
--

CREATE TABLE `catalog_categories` (
  `id` int(11) NOT NULL,
  `name_DE` varchar(200) NOT NULL,
  `name_EN` varchar(200) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `market_player`
--

CREATE TABLE `market_player` (
  `id` int(11) DEFAULT NULL,
  `id_mastr` varchar(50) NOT NULL,
  `ts_last_update` timestamp NULL DEFAULT NULL,
  `id_persona` int(11) DEFAULT NULL,
  `id_salutation` int(11) DEFAULT NULL,
  `id_title` int(11) DEFAULT NULL,
  `first_name` varchar(300) DEFAULT NULL,
  `last_name` varchar(300) DEFAULT NULL,
  `company_name` varchar(300) DEFAULT NULL,
  `id_role` int(11) DEFAULT NULL,
  `id_legal_form` int(11) DEFAULT NULL,
  `id_other_form` varchar(200) DEFAULT NULL,
  `id_market_roles` varchar(200) DEFAULT NULL,
  `representative` varchar(200) DEFAULT NULL,
  `id_country` int(11) DEFAULT NULL,
  `region` varchar(200) DEFAULT NULL,
  `street` varchar(200) DEFAULT NULL,
  `street_nr` varchar(5) DEFAULT NULL,
  `no_street` tinyint(4) DEFAULT NULL,
  `address_extra` varchar(200) DEFAULT NULL,
  `zipcode` varchar(10) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `id_state` int(11) DEFAULT NULL,
  `id_grid_operator` int(11) DEFAULT NULL,
  `nuts2` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` varchar(100) DEFAULT NULL,
  `fax` varchar(100) DEFAULT NULL,
  `no_fax` tinyint(4) DEFAULT NULL,
  `website` varchar(100) DEFAULT NULL,
  `no_website` tinyint(4) DEFAULT NULL,
  `id_court` int(11) DEFAULT NULL,
  `no_court` tinyint(4) DEFAULT NULL,
  `foreign_court` varchar(100) DEFAULT NULL,
  `no_foreign_court` tinyint(4) DEFAULT NULL,
  `registration_nr` varchar(100) DEFAULT NULL,
  `no_registration_nr` tinyint(4) DEFAULT NULL,
  `foreign_registration_nr` varchar(100) DEFAULT NULL,
  `no_foreign_registration_nr` tinyint(4) DEFAULT NULL,
  `date_start_operation` date DEFAULT NULL,
  `acer_code` varchar(50) DEFAULT NULL,
  `no_acer_code` tinyint(4) DEFAULT NULL,
  `sales_tax_id` varchar(50) DEFAULT NULL,
  `no_sales_tax_id` tinyint(4) DEFAULT NULL,
  `date_end_operation` date DEFAULT NULL,
  `no_date_end_operation` tinyint(4) DEFAULT NULL,
  `bundesnetzagentur_id` varchar(50) DEFAULT NULL,
  `no_bundesnetzagentur_id` tinyint(4) NOT NULL,
  `id_postal_country` int(11) DEFAULT NULL,
  `postal_zip` varchar(10) DEFAULT NULL,
  `postal_city` varchar(100) DEFAULT NULL,
  `postal_street` varchar(200) DEFAULT NULL,
  `postal_nr` varchar(5) DEFAULT NULL,
  `postal_no_nr` tinyint(4) DEFAULT NULL,
  `postal_extra_info` varchar(100) DEFAULT NULL,
  `small_company_kmu` tinyint(4) DEFAULT NULL,
  `phone_vmav` varchar(100) DEFAULT NULL,
  `email_vmav` varchar(100) DEFAULT NULL,
  `date_registration` date DEFAULT NULL,
  `id_industry_dept` int(11) DEFAULT NULL,
  `id_industry_group` int(11) DEFAULT NULL,
  `id_industry_section` int(11) DEFAULT NULL,
  `is_direct_marketer` tinyint(4) NOT NULL,
  `is_electricity_supplier_customer` tinyint(4) DEFAULT NULL,
  `is_electricity_supplier_households` tinyint(4) DEFAULT NULL,
  `is_gas_trader` tinyint(4) DEFAULT NULL,
  `is_electricity_trader` tinyint(4) DEFAULT NULL,
  `is_gas_supplier` tinyint(4) NOT NULL,
  `is_gas_supplier_households` tinyint(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `market_roles`
--

CREATE TABLE `market_roles` (
  `id_mastr_role` varchar(50) NOT NULL,
  `market_role` varchar(200) NOT NULL,
  `ts_last_update` timestamp NULL DEFAULT NULL,
  `id_mastr_party` int(11) NOT NULL,
  `bnetza_nr` varchar(100) NOT NULL,
  `no_bnetza_nr` tinyint(4) NOT NULL,
  `id_market_partner` varchar(100) NOT NULL,
  `no_id_market_partner` tinyint(4) NOT NULL,
  `contact_role` varchar(500) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `power_units_nuclear`
--

CREATE TABLE `power_units_nuclear` (
  `id_mastr_unit` varchar(50) NOT NULL,
  `ts_last_update` timestamp NULL DEFAULT NULL,
  `id_mastr_market_location` varchar(50) DEFAULT NULL,
  `id_control_status` int(11) DEFAULT NULL,
  `ts_last_control` date DEFAULT NULL,
  `id_mastr_operator` varchar(50) DEFAULT NULL,
  `id_country` int(11) DEFAULT NULL,
  `id_state` int(11) DEFAULT NULL,
  `region` varchar(100) DEFAULT NULL,
  `municipality` varchar(100) DEFAULT NULL,
  `id_municipality` varchar(50) DEFAULT NULL,
  `zipcode` varchar(10) DEFAULT NULL,
  `communal_district` varchar(100) DEFAULT NULL,
  `id_land_parcel` varchar(50) DEFAULT NULL,
  `street` varchar(100) DEFAULT NULL,
  `no_street` tinyint(4) DEFAULT NULL,
  `street_nr` varchar(10) DEFAULT NULL,
  `no_street_nr` tinyint(4) DEFAULT NULL,
  `street_not_found` tinyint(4) DEFAULT NULL,
  `address_extra` int(11) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `longitude` decimal(12,7) DEFAULT NULL,
  `latitude` decimal(12,7) DEFAULT NULL,
  `date_register` date DEFAULT NULL,
  `date_commissioning_planned` date DEFAULT NULL,
  `date_commissioning` date DEFAULT NULL,
  `date_final_decommissioning` date DEFAULT NULL,
  `date_temp_decommissioning` date DEFAULT NULL,
  `date_restart_operation` int(11) DEFAULT NULL,
  `id_status_system` int(11) DEFAULT NULL,
  `id_status_operation` int(11) DEFAULT NULL,
  `id_mastr_legacy` varchar(50) DEFAULT NULL,
  `not_in_migrated_units` tinyint(4) DEFAULT NULL,
  `id_mastr_last_operator` varchar(50) DEFAULT NULL,
  `date_operator_change` date DEFAULT NULL,
  `date_operator_change_register` date DEFAULT NULL,
  `name` varchar(200) DEFAULT NULL,
  `weic` varchar(50) DEFAULT NULL,
  `no_weic` tinyint(4) DEFAULT NULL,
  `weic_display_name` varchar(100) DEFAULT NULL,
  `id_bnetza_nr` varchar(50) DEFAULT NULL,
  `no_bnetza_nr` tinyint(4) DEFAULT NULL,
  `id_primary_energy` int(11) DEFAULT NULL,
  `power_brutto` decimal(15,3) DEFAULT NULL,
  `power_netto` decimal(15,3) DEFAULT NULL,
  `is_connected_high_voltage` tinyint(4) DEFAULT NULL,
  `is_blackstart_ready` tinyint(4) DEFAULT NULL,
  `is_island_operation_ready` tinyint(4) DEFAULT NULL,
  `id_market_partner` varchar(50) DEFAULT NULL,
  `remote_control_grid_operator` tinyint(4) DEFAULT NULL,
  `remote_control_direct_marketer` tinyint(4) DEFAULT NULL,
  `remote_control_third_party` tinyint(4) DEFAULT NULL,
  `id_infeed_type` int(11) DEFAULT NULL,
  `prequalified_balancing` tinyint(4) DEFAULT NULL,
  `id_mastr_approval` varchar(50) DEFAULT NULL,
  `name_power_plant` varchar(100) DEFAULT NULL,
  `name_power_unit` varchar(100) DEFAULT NULL,
  `id_technology` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `power_units_solar`
--

CREATE TABLE `power_units_solar` (
  `id_mastr_unit` varchar(50) NOT NULL,
  `ts_last_update` timestamp NULL DEFAULT NULL,
  `id_mastr_market_location` varchar(50) DEFAULT NULL,
  `id_control_status` int(11) DEFAULT NULL,
  `ts_last_control` date DEFAULT NULL,
  `id_mastr_operator` varchar(50) DEFAULT NULL,
  `id_country` int(11) DEFAULT NULL,
  `id_state` int(11) DEFAULT NULL,
  `region` varchar(100) DEFAULT NULL,
  `municipality` varchar(100) DEFAULT NULL,
  `id_municipality` varchar(50) DEFAULT NULL,
  `zipcode` varchar(10) DEFAULT NULL,
  `communal_district` varchar(100) DEFAULT NULL,
  `id_land_parcel` varchar(50) DEFAULT NULL,
  `street` varchar(100) DEFAULT NULL,
  `no_street` tinyint(4) DEFAULT NULL,
  `street_nr` varchar(10) DEFAULT NULL,
  `no_street_nr` tinyint(4) DEFAULT NULL,
  `street_not_found` tinyint(4) DEFAULT NULL,
  `address_extra` int(11) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `longitude` decimal(12,7) DEFAULT NULL,
  `latitude` decimal(12,7) DEFAULT NULL,
  `date_register` date DEFAULT NULL,
  `date_commissioning_planned` date DEFAULT NULL,
  `date_commissioning` date DEFAULT NULL,
  `date_final_decommissioning` date DEFAULT NULL,
  `date_temp_decommissioning` date DEFAULT NULL,
  `date_restart_operation` int(11) DEFAULT NULL,
  `id_status_system` int(11) DEFAULT NULL,
  `id_status_operation` int(11) DEFAULT NULL,
  `id_mastr_legacy` varchar(50) DEFAULT NULL,
  `not_in_migrated_units` tinyint(4) DEFAULT NULL,
  `id_mastr_last_operator` varchar(50) DEFAULT NULL,
  `date_operator_change` date DEFAULT NULL,
  `date_operator_change_register` date DEFAULT NULL,
  `name` varchar(200) DEFAULT NULL,
  `weic` varchar(50) DEFAULT NULL,
  `no_weic` tinyint(4) DEFAULT NULL,
  `weic_display_name` varchar(100) DEFAULT NULL,
  `id_bnetza_nr` varchar(50) DEFAULT NULL,
  `no_bnetza_nr` tinyint(4) DEFAULT NULL,
  `id_primary_energy` int(11) DEFAULT NULL,
  `power_brutto` decimal(15,3) DEFAULT NULL,
  `power_netto` decimal(15,3) DEFAULT NULL,
  `is_connected_high_voltage` tinyint(4) DEFAULT NULL,
  `is_blackstart_ready` tinyint(4) DEFAULT NULL,
  `is_island_operation_ready` tinyint(4) DEFAULT NULL,
  `id_market_partner` varchar(50) DEFAULT NULL,
  `remote_control_grid_operator` tinyint(4) DEFAULT NULL,
  `remote_control_direct_marketer` tinyint(4) DEFAULT NULL,
  `remote_control_third_party` tinyint(4) DEFAULT NULL,
  `id_infeed_type` int(11) DEFAULT NULL,
  `prequalified_balancing` tinyint(4) DEFAULT NULL,
  `id_mastr_approval` varchar(50) DEFAULT NULL,
  `power_converter` decimal(15,3) DEFAULT NULL,
  `id_converter_storage` int(11) DEFAULT NULL,
  `nr_modules` int(6) DEFAULT NULL,
  `id_location_type` int(11) DEFAULT NULL,
  `id_power_curtailment` int(11) DEFAULT NULL,
  `has_common_angle` tinyint(4) DEFAULT NULL,
  `id_main_direction` int(11) DEFAULT NULL,
  `id_main_angle` int(11) DEFAULT NULL,
  `id_secondary_direction` int(11) DEFAULT NULL,
  `id_secondary_angle` int(11) DEFAULT NULL,
  `area_used` decimal(15,3) DEFAULT NULL,
  `id_area_type` varchar(100) DEFAULT NULL,
  `area_used_agriculture` decimal(15,3) DEFAULT NULL,
  `id_usage_of_location` int(11) DEFAULT NULL,
  `id_mastr_eeg` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `power_units_thermal`
--

CREATE TABLE `power_units_thermal` (
  `id_mastr_unit` varchar(50) NOT NULL,
  `ts_last_update` timestamp NULL DEFAULT NULL,
  `id_mastr_market_location` varchar(50) DEFAULT NULL,
  `id_control_status` int(11) DEFAULT NULL,
  `ts_last_control` date DEFAULT NULL,
  `id_mastr_operator` varchar(50) DEFAULT NULL,
  `id_country` int(11) DEFAULT NULL,
  `id_state` int(11) DEFAULT NULL,
  `region` varchar(100) DEFAULT NULL,
  `municipality` varchar(100) DEFAULT NULL,
  `id_municipality` varchar(50) DEFAULT NULL,
  `zipcode` varchar(10) DEFAULT NULL,
  `communal_district` varchar(100) DEFAULT NULL,
  `id_land_parcel` varchar(50) DEFAULT NULL,
  `street` varchar(100) DEFAULT NULL,
  `no_street` tinyint(4) DEFAULT NULL,
  `street_nr` varchar(10) DEFAULT NULL,
  `no_street_nr` tinyint(4) DEFAULT NULL,
  `street_not_found` tinyint(4) DEFAULT NULL,
  `address_extra` int(11) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `longitude` decimal(12,7) DEFAULT NULL,
  `latitude` decimal(12,7) DEFAULT NULL,
  `date_register` date DEFAULT NULL,
  `date_commissioning_planned` date DEFAULT NULL,
  `date_commissioning` date DEFAULT NULL,
  `date_final_decommissioning` date DEFAULT NULL,
  `date_temp_decommissioning` date DEFAULT NULL,
  `date_restart_operation` int(11) DEFAULT NULL,
  `id_status_system` int(11) DEFAULT NULL,
  `id_status_operation` int(11) DEFAULT NULL,
  `id_mastr_legacy` varchar(50) DEFAULT NULL,
  `not_in_migrated_units` tinyint(4) DEFAULT NULL,
  `id_mastr_last_operator` varchar(50) DEFAULT NULL,
  `date_operator_change` date DEFAULT NULL,
  `date_operator_change_register` date DEFAULT NULL,
  `name` varchar(200) DEFAULT NULL,
  `weic` varchar(50) DEFAULT NULL,
  `no_weic` tinyint(4) DEFAULT NULL,
  `weic_display_name` varchar(100) DEFAULT NULL,
  `id_bnetza_nr` varchar(50) DEFAULT NULL,
  `no_bnetza_nr` tinyint(4) DEFAULT NULL,
  `id_primary_energy` int(11) DEFAULT NULL,
  `power_brutto` decimal(15,3) DEFAULT NULL,
  `power_netto` decimal(15,3) DEFAULT NULL,
  `is_connected_high_voltage` tinyint(4) DEFAULT NULL,
  `is_blackstart_ready` tinyint(4) DEFAULT NULL,
  `is_island_operation_ready` tinyint(4) DEFAULT NULL,
  `id_market_partner` varchar(50) DEFAULT NULL,
  `remote_control_grid_operator` tinyint(4) DEFAULT NULL,
  `remote_control_direct_marketer` tinyint(4) DEFAULT NULL,
  `remote_control_third_party` tinyint(4) DEFAULT NULL,
  `id_infeed_type` int(11) DEFAULT NULL,
  `prequalified_balancing` tinyint(4) DEFAULT NULL,
  `id_mastr_approval` varchar(50) DEFAULT NULL,
  `id_technology` int(11) DEFAULT NULL,
  `name_power_plant` varchar(100) DEFAULT NULL,
  `name_power_unit` varchar(100) DEFAULT NULL,
  `date_construction_start` date DEFAULT NULL,
  `has_reported_operation_end` tinyint(4) DEFAULT NULL,
  `id_operation_end` int(11) DEFAULT NULL,
  `date_end_operation` date DEFAULT NULL,
  `power_added_combi_operation` decimal(15,3) DEFAULT NULL,
  `is_in_combi_operation` tinyint(4) DEFAULT NULL,
  `id_mastr_combi_operation` varchar(50) DEFAULT NULL,
  `date_grid_reserve_start` date DEFAULT NULL,
  `date_emergency_reserve_start` date DEFAULT NULL,
  `id_other_primary_energy` int(11) DEFAULT NULL,
  `id_other_fuels` int(11) DEFAULT NULL,
  `is_border_power_plant` tinyint(4) DEFAULT NULL,
  `power_netto_max_germany` decimal(15,3) DEFAULT NULL,
  `contracted_consumers` varchar(500) DEFAULT NULL,
  `is_backup_power` tinyint(4) DEFAULT NULL,
  `id_location_backup_power` int(11) DEFAULT NULL,
  `id_mastr_kwk` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `power_units_wind`
--

CREATE TABLE `power_units_wind` (
  `id_mastr_unit` varchar(50) NOT NULL,
  `ts_last_update` timestamp NULL DEFAULT NULL,
  `id_mastr_market_location` varchar(50) DEFAULT NULL,
  `id_control_status` int(11) DEFAULT NULL,
  `ts_last_control` date DEFAULT NULL,
  `id_mastr_operator` varchar(50) DEFAULT NULL,
  `id_country` int(11) DEFAULT NULL,
  `id_state` int(11) DEFAULT NULL,
  `region` varchar(100) DEFAULT NULL,
  `municipality` varchar(100) DEFAULT NULL,
  `id_municipality` varchar(50) DEFAULT NULL,
  `zipcode` varchar(10) DEFAULT NULL,
  `communal_district` varchar(100) DEFAULT NULL,
  `id_land_parcel` varchar(50) DEFAULT NULL,
  `street` varchar(100) DEFAULT NULL,
  `no_street` tinyint(4) DEFAULT NULL,
  `street_nr` varchar(10) DEFAULT NULL,
  `no_street_nr` tinyint(4) DEFAULT NULL,
  `street_not_found` tinyint(4) DEFAULT NULL,
  `address_extra` int(11) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `longitude` decimal(12,7) DEFAULT NULL,
  `latitude` decimal(12,7) DEFAULT NULL,
  `date_register` date DEFAULT NULL,
  `date_commissioning_planned` date DEFAULT NULL,
  `date_commissioning` date DEFAULT NULL,
  `date_final_decommissioning` date DEFAULT NULL,
  `date_temp_decommissioning` date DEFAULT NULL,
  `date_restart_operation` int(11) DEFAULT NULL,
  `id_status_system` int(11) DEFAULT NULL,
  `id_status_operation` int(11) DEFAULT NULL,
  `id_mastr_legacy` varchar(50) DEFAULT NULL,
  `not_in_migrated_units` tinyint(4) DEFAULT NULL,
  `id_mastr_last_operator` varchar(50) DEFAULT NULL,
  `date_operator_change` date DEFAULT NULL,
  `date_operator_change_register` date DEFAULT NULL,
  `name` varchar(200) DEFAULT NULL,
  `weic` varchar(50) DEFAULT NULL,
  `no_weic` tinyint(4) DEFAULT NULL,
  `weic_display_name` varchar(100) DEFAULT NULL,
  `id_bnetza_nr` varchar(50) DEFAULT NULL,
  `no_bnetza_nr` tinyint(4) DEFAULT NULL,
  `id_primary_energy` int(11) DEFAULT NULL,
  `power_brutto` decimal(15,3) DEFAULT NULL,
  `power_netto` decimal(15,3) DEFAULT NULL,
  `is_connected_high_voltage` tinyint(4) DEFAULT NULL,
  `is_blackstart_ready` tinyint(4) DEFAULT NULL,
  `is_island_operation_ready` tinyint(4) DEFAULT NULL,
  `id_market_partner` varchar(50) DEFAULT NULL,
  `remote_control_grid_operator` tinyint(4) DEFAULT NULL,
  `remote_control_direct_marketer` tinyint(4) DEFAULT NULL,
  `remote_control_third_party` tinyint(4) DEFAULT NULL,
  `id_infeed_type` int(11) DEFAULT NULL,
  `prequalified_balancing` tinyint(4) DEFAULT NULL,
  `id_mastr_approval` varchar(50) DEFAULT NULL,
  `name_windpark` varchar(100) DEFAULT NULL,
  `id_location_type` int(11) DEFAULT NULL,
  `id_location_sea` int(11) DEFAULT NULL,
  `id_cluster_sea` int(11) DEFAULT NULL,
  `id_manufacturer` int(11) DEFAULT NULL,
  `id_technology` int(11) DEFAULT NULL,
  `name_type` varchar(100) DEFAULT NULL,
  `hub_height` decimal(15,3) DEFAULT NULL,
  `rotor_diameter` decimal(15,3) DEFAULT NULL,
  `has_deicing_system` tinyint(4) DEFAULT NULL,
  `has_restrictions` tinyint(4) DEFAULT NULL,
  `has_restrictions_sound_night` tinyint(4) DEFAULT NULL,
  `has_restrictions_sound_day` tinyint(4) DEFAULT NULL,
  `has_restrictions_shadow` tinyint(4) DEFAULT NULL,
  `has_restrictions_animals` tinyint(4) DEFAULT NULL,
  `has_restrictions_falling_ice` tinyint(4) DEFAULT NULL,
  `has_restrictions_other` tinyint(4) DEFAULT NULL,
  `water_depth` decimal(15,3) DEFAULT NULL,
  `distance_to_shore` decimal(15,3) DEFAULT NULL,
  `id_mastr_eeg` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Tabellenstruktur für Tabelle `zip_codes`
--

CREATE TABLE `zip_codes` (
  `plz` int(5) NOT NULL,
  `name` varchar(84) DEFAULT NULL,
  `population` int(9) DEFAULT NULL,
  `area` decimal(15,3) DEFAULT NULL,
  `lat` decimal(15,6) DEFAULT NULL,
  `lon` decimal(15,6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Indizes der exportierten Tabellen
--

--
-- Indizes für die Tabelle `balancing_areas`
--
ALTER TABLE `balancing_areas`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `catalog`
--
ALTER TABLE `catalog`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `catalog_categories`
--
ALTER TABLE `catalog_categories`
  ADD PRIMARY KEY (`id`);

--
-- Indizes für die Tabelle `market_player`
--
ALTER TABLE `market_player`
  ADD PRIMARY KEY (`id_mastr`);

--
-- Indizes für die Tabelle `market_roles`
--
ALTER TABLE `market_roles`
  ADD PRIMARY KEY (`id_mastr_role`);

--
-- Indizes für die Tabelle `power_units_nuclear`
--
ALTER TABLE `power_units_nuclear`
  ADD PRIMARY KEY (`id_mastr_unit`);

--
-- Indizes für die Tabelle `power_units_solar`
--
ALTER TABLE `power_units_solar`
  ADD PRIMARY KEY (`id_mastr_unit`);

--
-- Indizes für die Tabelle `power_units_thermal`
--
ALTER TABLE `power_units_thermal`
  ADD PRIMARY KEY (`id_mastr_unit`);

--
-- Indizes für die Tabelle `power_units_wind`
--
ALTER TABLE `power_units_wind`
  ADD PRIMARY KEY (`id_mastr_unit`);

--
-- Indizes für die Tabelle `zip_codes`
--
ALTER TABLE `zip_codes`
  ADD PRIMARY KEY (`plz`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
