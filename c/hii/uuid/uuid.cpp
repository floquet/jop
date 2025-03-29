#include <iostream>
#include <random>
#include <vector>
#include <iomanip>
#include <algorithm>
#include <functional>
#include <optional>
#include <array>

class UUIDGenerator {
public:
    static constexpr size_t UUID_SIZE = 16; // UUID size in bytes (16 * 8 = 128 bits)

    // Generates a UUID v4 (random)
    static std::array<uint8_t, UUID_SIZE> generateUUID(
        std::optional<std::vector<uint32_t>> seed = std::nullopt,
        std::optional<bool> checkOS = std::nullopt) {
        
        std::array<uint8_t, UUID_SIZE> uuid;
        
        // Initialize random number generator
        std::random_device rd;
        std::mt19937 gen(rd());
        
        // If seed is provided, use it
        if (seed.has_value()) {
            std::seed_seq seed_seq(seed->begin(), seed->end());
            gen.seed(seed_seq);
        }
        // If checkOS is true, rely on random_device for better entropy
        else if (checkOS.has_value() && checkOS.value()) {
            // random_device already used, nothing more needed
        }
        
        // Generate random bytes
        std::uniform_int_distribution<uint16_t> dist(0, 255);
        for (auto& byte : uuid) {
            byte = static_cast<uint8_t>(dist(gen));
        }
        
        // Set UUID version (v4: random) and variant (RFC 4122)
        uuid[6] = (uuid[6] & 0x0F) | 0x40; // Set version to 4
        uuid[8] = (uuid[8] & 0x3F) | 0x80; // Set variant to RFC 4122
        
        return uuid;
    }
    
    // Prints the UUID in standard hexadecimal format
    static void printUUID(const std::array<uint8_t, UUID_SIZE>& uuid) {
        for (size_t i = 0; i < uuid.size(); ++i) {
            std::cout << std::hex << std::setw(2) << std::setfill('0') 
                      << static_cast<int>(uuid[i]);
            if (i == 3 || i == 5 || i == 7 || i == 9) {
                std::cout << "-";
            }
        }
        std::cout << std::dec << std::endl;
    }
    
    // Compares two UUIDs
    static bool areUUIDsEqual(const std::array<uint8_t, UUID_SIZE>& uuid1, 
                             const std::array<uint8_t, UUID_SIZE>& uuid2) {
        return uuid1 == uuid2;
    }
    
    // Returns an empty UUID (all zeros)
    static std::array<uint8_t, UUID_SIZE> emptyUUID() {
        std::array<uint8_t, UUID_SIZE> uuid{};
        return uuid;
    }
};

int main() {
    // Example usage
    
    // Without seed (default initialization)
    auto uuid1 = UUIDGenerator::generateUUID();
    std::cout << "UUID1: ";
    UUIDGenerator::printUUID(uuid1);
    
    // With user-defined seed
    std::vector<uint32_t> seed = {12345, 67890, 13579, 24680};
    auto uuid2 = UUIDGenerator::generateUUID(seed);
    std::cout << "UUID2: ";
    UUIDGenerator::printUUID(uuid2);
    
    // With OS-based seeding (using random_device)
    auto uuid3 = UUIDGenerator::generateUUID(std::nullopt, true);
    std::cout << "UUID3: ";
    UUIDGenerator::printUUID(uuid3);
    
    // Compare UUIDs
    std::cout << "UUID1 == UUID2: " 
              << (UUIDGenerator::areUUIDsEqual(uuid1, uuid2) ? "true" : "false")
              << std::endl;
    
    // Empty UUID
    auto empty = UUIDGenerator::emptyUUID();
    std::cout << "Empty UUID: ";
    UUIDGenerator::printUUID(empty);
    
    return 0;
}