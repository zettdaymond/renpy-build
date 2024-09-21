#ifdef __cplusplus
extern "C" {
#endif

struct AuroraIntegrationHandle;

/**
 * @brief Initialize aurora integration:
 *
 *  - Setup SDL mouse events mapping on devices with vertical display
 *  - Capture audio resource
 *  - Prevent display blanking
 * 
 * @return AuraraIntegrationHandle - handle != NULL if initialization valid
 */
struct AuroraIntegrationHandle* AuroraIntergrationStartup();

/**
 * @brief Properly shutdown AuroraOS integration
 * 
 * @param handle - not NULL handle of previous initializtion
 */
void AuroraIntergrationShutdown(struct AuroraIntegrationHandle* handle);


#ifdef __cplusplus
}
#endif
