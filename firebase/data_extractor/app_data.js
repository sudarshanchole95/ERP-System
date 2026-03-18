const AppData = {
  init() {
    const initialized = localStorage.getItem('appInitialized');

    if (initialized === 'true') {
      console.log('App data already initialized.');
      return;
    }

    console.log('Initializing app data in Local Storage...');

    // Users Collection
    const users = [
      {
        id: "usr_mgmt_001",
        uid: "firebase_uid_mgmt_001",
        firstName: "Patricia",
        lastName: "Henderson",
        email: "patricia.henderson@gtvl.com",
        phone: "+1-555-0101",
        role: "management",
        employeeId: null,
        status: "active",
        createdAt: "2024-01-15T08:00:00Z",
        updatedAt: "2024-01-15T08:00:00Z"
      },
      {
        id: "usr_mgmt_002",
        uid: "firebase_uid_mgmt_002",
        firstName: "Michael",
        lastName: "Torres",
        email: "michael.torres@gtvl.com",
        phone: "+1-555-0102",
        role: "management",
        employeeId: null,
        status: "active",
        createdAt: "2024-01-20T09:30:00Z",
        updatedAt: "2024-01-20T09:30:00Z"
      },
      {
        id: "usr_sup_001",
        uid: "firebase_uid_sup_001",
        firstName: "Sarah",
        lastName: "Mitchell",
        email: "sarah.mitchell@gtvl.com",
        phone: "+1-555-0201",
        role: "supervisor",
        employeeId: "SUP-2024-001",
        status: "active",
        createdAt: "2024-02-01T10:00:00Z",
        updatedAt: "2024-02-01T10:00:00Z"
      },
      {
        id: "usr_sup_002",
        uid: "firebase_uid_sup_002",
        firstName: "David",
        lastName: "Chen",
        email: "david.chen@gtvl.com",
        phone: "+1-555-0202",
        role: "supervisor",
        employeeId: "SUP-2024-002",
        status: "active",
        createdAt: "2024-02-05T11:15:00Z",
        updatedAt: "2024-02-05T11:15:00Z"
      },
      {
        id: "usr_sup_003",
        uid: "firebase_uid_sup_003",
        firstName: "Jennifer",
        lastName: "Rodriguez",
        email: "jennifer.rodriguez@gtvl.com",
        phone: "+1-555-0203",
        role: "supervisor",
        employeeId: "SUP-2024-003",
        status: "active",
        createdAt: "2024-02-10T08:45:00Z",
        updatedAt: "2024-02-10T08:45:00Z"
      },
      {
        id: "usr_promo_001",
        uid: "firebase_uid_promo_001",
        firstName: "Marcus",
        lastName: "Johnson",
        email: "marcus.johnson@gtvl.com",
        phone: "+1-555-0301",
        role: "promodizer",
        employeeId: "PRO-2024-001",
        status: "active",
        createdAt: "2024-03-01T09:00:00Z",
        updatedAt: "2024-03-01T09:00:00Z"
      },
      {
        id: "usr_promo_002",
        uid: "firebase_uid_promo_002",
        firstName: "Emily",
        lastName: "Thompson",
        email: "emily.thompson@gtvl.com",
        phone: "+1-555-0302",
        role: "promodizer",
        employeeId: "PRO-2024-002",
        status: "active",
        createdAt: "2024-03-03T10:30:00Z",
        updatedAt: "2024-03-03T10:30:00Z"
      },
      {
        id: "usr_promo_003",
        uid: "firebase_uid_promo_003",
        firstName: "Carlos",
        lastName: "Martinez",
        email: "carlos.martinez@gtvl.com",
        phone: "+1-555-0303",
        role: "promodizer",
        employeeId: "PRO-2024-003",
        status: "active",
        createdAt: "2024-03-05T11:00:00Z",
        updatedAt: "2024-03-05T11:00:00Z"
      },
      {
        id: "usr_promo_004",
        uid: "firebase_uid_promo_004",
        firstName: "Lisa",
        lastName: "Anderson",
        email: "lisa.anderson@gtvl.com",
        phone: "+1-555-0304",
        role: "promodizer",
        employeeId: "PRO-2024-004",
        status: "active",
        createdAt: "2024-03-07T09:45:00Z",
        updatedAt: "2024-03-07T09:45:00Z"
      },
      {
        id: "usr_promo_005",
        uid: "firebase_uid_promo_005",
        firstName: "James",
        lastName: "Wilson",
        email: "james.wilson@gtvl.com",
        phone: "+1-555-0305",
        role: "promodizer",
        employeeId: "PRO-2024-005",
        status: "active",
        createdAt: "2024-03-10T08:30:00Z",
        updatedAt: "2024-03-10T08:30:00Z"
      },
      {
        id: "usr_promo_006",
        uid: "firebase_uid_promo_006",
        firstName: "Nina",
        lastName: "Patel",
        email: "nina.patel@gtvl.com",
        phone: "+1-555-0306",
        role: "promodizer",
        employeeId: "PRO-2024-006",
        status: "active",
        createdAt: "2024-03-12T10:00:00Z",
        updatedAt: "2024-03-12T10:00:00Z"
      },
      {
        id: "usr_sales_001",
        uid: "firebase_uid_sales_001",
        firstName: "Robert",
        lastName: "Davis",
        email: "robert.davis@gtvl.com",
        phone: "+1-555-0401",
        role: "salesOperations",
        employeeId: null,
        status: "active",
        createdAt: "2024-01-25T09:00:00Z",
        updatedAt: "2024-01-25T09:00:00Z"
      },
      {
        id: "usr_sales_002",
        uid: "firebase_uid_sales_002",
        firstName: "Amanda",
        lastName: "Lee",
        email: "amanda.lee@gtvl.com",
        phone: "+1-555-0402",
        role: "salesOperations",
        employeeId: null,
        status: "active",
        createdAt: "2024-02-01T10:30:00Z",
        updatedAt: "2024-02-01T10:30:00Z"
      }
    ];

    // SKUs Collection
    const skus = [
      {
        id: "sku_001",
        skuCode: "GTVL-SNACK-001",
        barcode: "8901234567890",
        productName: "Premium Potato Chips - Sea Salt",
        description: "Crispy potato chips with natural sea salt seasoning, 150g pack",
        category: "Snacks",
        unitPrice: 3.99,
        status: "active",
        createdAt: "2024-01-10T08:00:00Z",
        updatedAt: "2024-01-10T08:00:00Z"
      },
      {
        id: "sku_002",
        skuCode: "GTVL-SNACK-002",
        barcode: "8901234567891",
        productName: "Premium Potato Chips - BBQ",
        description: "Crispy potato chips with smoky BBQ flavor, 150g pack",
        category: "Snacks",
        unitPrice: 3.99,
        status: "active",
        createdAt: "2024-01-10T08:15:00Z",
        updatedAt: "2024-01-10T08:15:00Z"
      },
      {
        id: "sku_003",
        skuCode: "GTVL-BEV-001",
        barcode: "8901234567892",
        productName: "Energy Drink - Original",
        description: "Sugar-free energy drink with vitamins B & C, 250ml can",
        category: "Beverages",
        unitPrice: 2.49,
        status: "active",
        createdAt: "2024-01-12T09:00:00Z",
        updatedAt: "2024-01-12T09:00:00Z"
      },
      {
        id: "sku_004",
        skuCode: "GTVL-BEV-002",
        barcode: "8901234567893",
        productName: "Energy Drink - Tropical",
        description: "Sugar-free tropical flavor energy drink, 250ml can",
        category: "Beverages",
        unitPrice: 2.49,
        status: "active",
        createdAt: "2024-01-12T09:15:00Z",
        updatedAt: "2024-01-12T09:15:00Z"
      },
      {
        id: "sku_005",
        skuCode: "GTVL-CONF-001",
        barcode: "8901234567894",
        productName: "Chocolate Bar - Dark 70%",
        description: "Premium dark chocolate with 70% cocoa, 100g bar",
        category: "Confectionery",
        unitPrice: 4.99,
        status: "active",
        createdAt: "2024-01-15T10:00:00Z",
        updatedAt: "2024-01-15T10:00:00Z"
      },
      {
        id: "sku_006",
        skuCode: "GTVL-CONF-002",
        barcode: "8901234567895",
        productName: "Chocolate Bar - Milk Hazelnut",
        description: "Creamy milk chocolate with roasted hazelnuts, 100g bar",
        category: "Confectionery",
        unitPrice: 4.49,
        status: "active",
        createdAt: "2024-01-15T10:15:00Z",
        updatedAt: "2024-01-15T10:15:00Z"
      },
      {
        id: "sku_007",
        skuCode: "GTVL-SNACK-003",
        barcode: "8901234567896",
        productName: "Protein Bar - Chocolate Peanut",
        description: "High protein bar with chocolate and peanut flavor, 60g",
        category: "Snacks",
        unitPrice: 2.99,
        status: "active",
        createdAt: "2024-01-18T11:00:00Z",
        updatedAt: "2024-01-18T11:00:00Z"
      },
      {
        id: "sku_008",
        skuCode: "GTVL-BEV-003",
        barcode: "8901234567897",
        productName: "Sparkling Water - Lemon",
        description: "Zero calorie sparkling water with natural lemon flavor, 500ml",
        category: "Beverages",
        unitPrice: 1.99,
        status: "active",
        createdAt: "2024-01-20T09:00:00Z",
        updatedAt: "2024-01-20T09:00:00Z"
      },
      {
        id: "sku_009",
        skuCode: "GTVL-CONF-003",
        barcode: "8901234567898",
        productName: "Gummy Bears - Mixed Fruit",
        description: "Soft and chewy gummy bears in assorted fruit flavors, 200g",
        category: "Confectionery",
        unitPrice: 3.49,
        status: "active",
        createdAt: "2024-01-22T10:30:00Z",
        updatedAt: "2024-01-22T10:30:00Z"
      },
      {
        id: "sku_010",
        skuCode: "GTVL-SNACK-004",
        barcode: "8901234567899",
        productName: "Trail Mix - Deluxe",
        description: "Premium mix of nuts, dried fruits, and dark chocolate, 250g",
        category: "Snacks",
        unitPrice: 6.99,
        status: "active",
        createdAt: "2024-01-25T11:00:00Z",
        updatedAt: "2024-01-25T11:00:00Z"
      },
      {
        id: "sku_011",
        skuCode: "GTVL-BEV-004",
        barcode: "8901234567900",
        productName: "Cold Brew Coffee - Original",
        description: "Ready-to-drink cold brew coffee, unsweetened, 330ml",
        category: "Beverages",
        unitPrice: 3.49,
        status: "active",
        createdAt: "2024-01-28T08:30:00Z",
        updatedAt: "2024-01-28T08:30:00Z"
      },
      {
        id: "sku_012",
        skuCode: "GTVL-SNACK-005",
        barcode: "8901234567901",
        productName: "Popcorn - Caramel",
        description: "Sweet caramel-coated popcorn, 120g resealable bag",
        category: "Snacks",
        unitPrice: 4.29,
        status: "active",
        createdAt: "2024-02-01T09:00:00Z",
        updatedAt: "2024-02-01T09:00:00Z"
      }
    ];

    // Stores Collection
    const stores = [
      {
        id: "store_001",
        storeCode: "NYC-DT-001",
        storeName: "Downtown Market NYC",
        address: {
          street: "455 Madison Avenue",
          city: "New York",
          state: "NY",
          zipCode: "10022",
          country: "USA"
        },
        contactPerson: "John Williams",
        phone: "+1-212-555-0101",
        email: "contact@downtownmarketnyc.com",
        status: "active",
        createdAt: "2024-01-05T08:00:00Z",
        updatedAt: "2024-01-05T08:00:00Z"
      },
      {
        id: "store_002",
        storeCode: "LA-BH-001",
        storeName: "Beverly Hills Grocery",
        address: {
          street: "9876 Wilshire Boulevard",
          city: "Los Angeles",
          state: "CA",
          zipCode: "90210",
          country: "USA"
        },
        contactPerson: "Maria Garcia",
        phone: "+1-310-555-0201",
        email: "info@bhgrocery.com",
        status: "active",
        createdAt: "2024-01-08T09:30:00Z",
        updatedAt: "2024-01-08T09:30:00Z"
      },
      {
        id: "store_003",
        storeCode: "CHI-LP-001",
        storeName: "Lincoln Park Superstore",
        address: {
          street: "2150 North Clark Street",
          city: "Chicago",
          state: "IL",
          zipCode: "60614",
          country: "USA"
        },
        contactPerson: "Thomas Brown",
        phone: "+1-773-555-0301",
        email: "manager@lpsuperstore.com",
        status: "active",
        createdAt: "2024-01-10T10:00:00Z",
        updatedAt: "2024-01-10T10:00:00Z"
      },
      {
        id: "store_004",
        storeCode: "MIA-SB-001",
        storeName: "South Beach Market",
        address: {
          street: "1550 Ocean Drive",
          city: "Miami Beach",
          state: "FL",
          zipCode: "33139",
          country: "USA"
        },
        contactPerson: "Sofia Martinez",
        phone: "+1-305-555-0401",
        email: "contact@southbeachmarket.com",
        status: "active",
        createdAt: "2024-01-12T11:00:00Z",
        updatedAt: "2024-01-12T11:00:00Z"
      },
      {
        id: "store_005",
        storeCode: "SEA-CP-001",
        storeName: "Capitol Hill Foods",
        address: {
          street: "720 East Pike Street",
          city: "Seattle",
          state: "WA",
          zipCode: "98122",
          country: "USA"
        },
        contactPerson: "Kevin Nguyen",
        phone: "+1-206-555-0501",
        email: "info@capitolhillfoods.com",
        status: "active",
        createdAt: "2024-01-15T08:30:00Z",
        updatedAt: "2024-01-15T08:30:00Z"
      },
      {
        id: "store_006",
        storeCode: "BOS-BC-001",
        storeName: "Beacon Hill Market",
        address: {
          street: "325 Charles Street",
          city: "Boston",
          state: "MA",
          zipCode: "02114",
          country: "USA"
        },
        contactPerson: "Patricia O'Brien",
        phone: "+1-617-555-0601",
        email: "contact@beaconhillmarket.com",
        status: "active",
        createdAt: "2024-01-18T09:00:00Z",
        updatedAt: "2024-01-18T09:00:00Z"
      },
      {
        id: "store_007",
        storeCode: "AUS-DT-001",
        storeName: "Downtown Austin Grocers",
        address: {
          street: "601 Congress Avenue",
          city: "Austin",
          state: "TX",
          zipCode: "78701",
          country: "USA"
        },
        contactPerson: "Daniel Rodriguez",
        phone: "+1-512-555-0701",
        email: "manager@austingrocers.com",
        status: "active",
        createdAt: "2024-01-20T10:30:00Z",
        updatedAt: "2024-01-20T10:30:00Z"
      }
    ];

    // Supervisor Allocations Collection
    const supervisorAllocations = [
      {
        id: "supalc_001",
        supervisorId: "usr_sup_001",
        storeId: "store_001",
        allocatedAt: "2024-02-05T09:00:00Z",
        createdAt: "2024-02-05T09:00:00Z"
      },
      {
        id: "supalc_002",
        supervisorId: "usr_sup_002",
        storeId: "store_002",
        allocatedAt: "2024-02-08T10:00:00Z",
        createdAt: "2024-02-08T10:00:00Z"
      },
      {
        id: "supalc_003",
        supervisorId: "usr_sup_003",
        storeId: "store_003",
        allocatedAt: "2024-02-12T11:00:00Z",
        createdAt: "2024-02-12T11:00:00Z"
      }
    ];

    // Promodizer Allocations Collection
    const promodizerAllocations = [
      {
        id: "proalc_001",
        promodizerId: "usr_promo_001",
        storeId: "store_001",
        supervisorId: "usr_sup_001",
        allocatedAt: "2024-03-05T09:00:00Z",
        createdAt: "2024-03-05T09:00:00Z"
      },
      {
        id: "proalc_002",
        promodizerId: "usr_promo_002",
        storeId: "store_001",
        supervisorId: "usr_sup_001",
        allocatedAt: "2024-03-06T10:00:00Z",
        createdAt: "2024-03-06T10:00:00Z"
      },
      {
        id: "proalc_003",
        promodizerId: "usr_promo_003",
        storeId: "store_002",
        supervisorId: "usr_sup_002",
        allocatedAt: "2024-03-08T09:30:00Z",
        createdAt: "2024-03-08T09:30:00Z"
      },
      {
        id: "proalc_004",
        promodizerId: "usr_promo_004",
        storeId: "store_002",
        supervisorId: "usr_sup_002",
        allocatedAt: "2024-03-09T11:00:00Z",
        createdAt: "2024-03-09T11:00:00Z"
      },
      {
        id: "proalc_005",
        promodizerId: "usr_promo_004",
        storeId: "store_003",
        supervisorId: "usr_sup_003",
        allocatedAt: "2024-03-10T10:00:00Z",
        createdAt: "2024-03-10T10:00:00Z"
      },
      {
        id: "proalc_006",
        promodizerId: "usr_promo_005",
        storeId: "store_003",
        supervisorId: "usr_sup_003",
        allocatedAt: "2024-03-12T09:00:00Z",
        createdAt: "2024-03-12T09:00:00Z"
      },
      {
        id: "proalc_007",
        promodizerId: "usr_promo_006",
        storeId: "store_004",
        supervisorId: null,
        allocatedAt: "2024-03-15T10:30:00Z",
        createdAt: "2024-03-15T10:30:00Z"
      },
      {
        id: "proalc_008",
        promodizerId: "usr_promo_001",
        storeId: "store_005",
        supervisorId: null,
        allocatedAt: "2024-03-18T11:00:00Z",
        createdAt: "2024-03-18T11:00:00Z"
      }
    ];

    // Sales Records Collection
    const salesRecords = [
      {
        id: "sale_001",
        submissionId: "batch_20241120_001",
        recordedById: "usr_promo_001",
        recordedByRole: "promodizer",
        storeId: "store_001",
        scannedSkus: [
          {
            skuId: "sku_001",
            barcode: "8901234567890",
            quantity: 5
          },
          {
            skuId: "sku_003",
            barcode: "8901234567892",
            quantity: 8
          },
          {
            skuId: "sku_005",
            barcode: "8901234567894",
            quantity: 3
          }
        ],
        recordedAt: "2024-11-20T10:15:00Z",
        createdAt: "2024-11-20T10:15:00Z"
      },
      {
        id: "sale_002",
        submissionId: "batch_20241120_002",
        recordedById: "usr_promo_002",
        recordedByRole: "promodizer",
        storeId: "store_001",
        scannedSkus: [
          {
            skuId: "sku_002",
            barcode: "8901234567891",
            quantity: 6
          },
          {
            skuId: "sku_004",
            barcode: "8901234567893",
            quantity: 10
          },
          {
            skuId: "sku_007",
            barcode: "8901234567896",
            quantity: 4
          }
        ],
        recordedAt: "2024-11-20T14:30:00Z",
        createdAt: "2024-11-20T14:30:00Z"
      },
      {
        id: "sale_003",
        submissionId: "batch_20241121_001",
        recordedById: "usr_sup_001",
        recordedByRole: "supervisor",
        storeId: "store_001",
        scannedSkus: [
          {
            skuId: "sku_006",
            barcode: "8901234567895",
            quantity: 7
          },
          {
            skuId: "sku_008",
            barcode: "8901234567897",
            quantity: 12
          }
        ],
        recordedAt: "2024-11-21T09:45:00Z",
        createdAt: "2024-11-21T09:45:00Z"
      },
      {
        id: "sale_004",
        submissionId: "batch_20241121_002",
        recordedById: "usr_promo_003",
        recordedByRole: "promodizer",
        storeId: "store_002",
        scannedSkus: [
          {
            skuId: "sku_001",
            barcode: "8901234567890",
            quantity: 9
          },
          {
            skuId: "sku_009",
            barcode: "8901234567898",
            quantity: 5
          },
          {
            skuId: "sku_010",
            barcode: "8901234567899",
            quantity: 2
          }
        ],
        recordedAt: "2024-11-21T11:20:00Z",
        createdAt: "2024-11-21T11:20:00Z"
      },
      {
        id: "sale_005",
        submissionId: "batch_20241121_003",
        recordedById: "usr_promo_004",
        recordedByRole: "promodizer",
        storeId: "store_002",
        scannedSkus: [
          {
            skuId: "sku_011",
            barcode: "8901234567900",
            quantity: 8
          },
          {
            skuId: "sku_012",
            barcode: "8901234567901",
            quantity: 6
          }
        ],
        recordedAt: "2024-11-21T15:00:00Z",
        createdAt: "2024-11-21T15:00:00Z"
      },
      {
        id: "sale_006",
        submissionId: "batch_20241122_001",
        recordedById: "usr_sup_002",
        recordedByRole: "supervisor",
        storeId: "store_002",
        scannedSkus: [
          {
            skuId: "sku_003",
            barcode: "8901234567892",
            quantity: 15
          },
          {
            skuId: "sku_005",
            barcode: "8901234567894",
            quantity: 4
          },
          {
            skuId: "sku_007",
            barcode: "8901234567896",
            quantity: 7
          }
        ],
        recordedAt: "2024-11-22T10:00:00Z",
        createdAt: "2024-11-22T10:00:00Z"
      },
      {
        id: "sale_007",
        submissionId: "batch_20241122_002",
        recordedById: "usr_promo_005",
        recordedByRole: "promodizer",
        storeId: "store_003",
        scannedSkus: [
          {
            skuId: "sku_001",
            barcode: "8901234567890",
            quantity: 11
          },
          {
            skuId: "sku_002",
            barcode: "8901234567891",
            quantity: 9
          },
          {
            skuId: "sku_008",
            barcode: "8901234567897",
            quantity: 14
          }
        ],
        recordedAt: "2024-11-22T13:30:00Z",
        createdAt: "2024-11-22T13:30:00Z"
      },
      {
        id: "sale_008",
        submissionId: "batch_20241123_001",
        recordedById: "usr_promo_004",
        recordedByRole: "promodizer",
        storeId: "store_003",
        scannedSkus: [
          {
            skuId: "sku_004",
            barcode: "8901234567893",
            quantity: 13
          },
          {
            skuId: "sku_006",
            barcode: "8901234567895",
            quantity: 5
          }
        ],
        recordedAt: "2024-11-23T09:15:00Z",
        createdAt: "2024-11-23T09:15:00Z"
      },
      {
        id: "sale_009",
        submissionId: "batch_20241123_002",
        recordedById: "usr_sup_003",
        recordedByRole: "supervisor",
        storeId: "store_003",
        scannedSkus: [
          {
            skuId: "sku_009",
            barcode: "8901234567898",
            quantity: 8
          },
          {
            skuId: "sku_010",
            barcode: "8901234567899",
            quantity: 3
          },
          {
            skuId: "sku_011",
            barcode: "8901234567900",
            quantity: 6
          }
        ],
        recordedAt: "2024-11-23T14:45:00Z",
        createdAt: "2024-11-23T14:45:00Z"
      },
      {
        id: "sale_010",
        submissionId: "batch_20241123_003",
        recordedById: "usr_promo_006",
        recordedByRole: "promodizer",
        storeId: "store_004",
        scannedSkus: [
          {
            skuId: "sku_002",
            barcode: "8901234567891",
            quantity: 7
          },
          {
            skuId: "sku_005",
            barcode: "8901234567894",
            quantity: 4
          },
          {
            skuId: "sku_012",
            barcode: "8901234567901",
            quantity: 9
          }
        ],
        recordedAt: "2024-11-23T16:00:00Z",
        createdAt: "2024-11-23T16:00:00Z"
      },
      {
        id: "sale_011",
        submissionId: "batch_20241124_001",
        recordedById: "usr_promo_001",
        recordedByRole: "promodizer",
        storeId: "store_005",
        scannedSkus: [
          {
            skuId: "sku_003",
            barcode: "8901234567892",
            quantity: 10
          },
          {
            skuId: "sku_007",
            barcode: "8901234567896",
            quantity: 5
          }
        ],
        recordedAt: "2024-11-24T08:30:00Z",
        createdAt: "2024-11-24T08:30:00Z"
      }
    ];

    // Attendance Records Collection
    const attendanceRecords = [
      {
        id: "att_001",
        userId: "usr_promo_001",
        userRole: "promodizer",
        date: "2024-11-20T00:00:00Z",
        storeId: "store_001",
        clockInTime: "2024-11-20T08:00:00Z",
        clockOutTime: "2024-11-20T17:00:00Z",
        status: "present",
        createdAt: "2024-11-20T08:00:00Z",
        updatedAt: "2024-11-20T17:00:00Z"
      },
      {
        id: "att_002",
        userId: "usr_promo_002",
        userRole: "promodizer",
        date: "2024-11-20T00:00:00Z",
        storeId: "store_001",
        clockInTime: "2024-11-20T08:15:00Z",
        clockOutTime: "2024-11-20T17:15:00Z",
        status: "present",
        createdAt: "2024-11-20T08:15:00Z",
        updatedAt: "2024-11-20T17:15:00Z"
      },
      {
        id: "att_003",
        userId: "usr_sup_001",
        userRole: "supervisor",
        date: "2024-11-20T00:00:00Z",
        storeId: "store_001",
        clockInTime: "2024-11-20T07:45:00Z",
        clockOutTime: "2024-11-20T18:00:00Z",
        status: "present",
        createdAt: "2024-11-20T07:45:00Z",
        updatedAt: "2024-11-20T18:00:00Z"
      },
      {
        id: "att_004",
        userId: "usr_promo_003",
        userRole: "promodizer",
        date: "2024-11-21T00:00:00Z",
        storeId: "store_002",
        clockInTime: "2024-11-21T08:30:00Z",
        clockOutTime: "2024-11-21T16:30:00Z",
        status: "present",
        createdAt: "2024-11-21T08:30:00Z",
        updatedAt: "2024-11-21T16:30:00Z"
      },
      {
        id: "att_005",
        userId: "usr_promo_004",
        userRole: "promodizer",
        date: "2024-11-21T00:00:00Z",
        storeId: "store_002",
        clockInTime: "2024-11-21T08:00:00Z",
        clockOutTime: "2024-11-21T17:00:00Z",
        status: "present",
        createdAt: "2024-11-21T08:00:00Z",
        updatedAt: "2024-11-21T17:00:00Z"
      },
      {
        id: "att_006",
        userId: "usr_sup_002",
        userRole: "supervisor",
        date: "2024-11-21T00:00:00Z",
        storeId: "store_002",
        clockInTime: "2024-11-21T07:30:00Z",
        clockOutTime: "2024-11-21T17:30:00Z",
        status: "present",
        createdAt: "2024-11-21T07:30:00Z",
        updatedAt: "2024-11-21T17:30:00Z"
      },
      {
        id: "att_007",
        userId: "usr_promo_005",
        userRole: "promodizer",
        date: "2024-11-22T00:00:00Z",
        storeId: "store_003",
        clockInTime: "2024-11-22T08:00:00Z",
        clockOutTime: "2024-11-22T16:45:00Z",
        status: "present",
        createdAt: "2024-11-22T08:00:00Z",
        updatedAt: "2024-11-22T16:45:00Z"
      },
      {
        id: "att_008",
        userId: "usr_promo_004",
        userRole: "promodizer",
        date: "2024-11-22T00:00:00Z",
        storeId: "store_003",
        clockInTime: "2024-11-22T08:15:00Z",
        clockOutTime: "2024-11-22T17:00:00Z",
        status: "present",
        createdAt: "2024-11-22T08:15:00Z",
        updatedAt: "2024-11-22T17:00:00Z"
      },
      {
        id: "att_009",
        userId: "usr_sup_003",
        userRole: "supervisor",
        date: "2024-11-22T00:00:00Z",
        storeId: "store_003",
        clockInTime: "2024-11-22T07:45:00Z",
        clockOutTime: "2024-11-22T18:15:00Z",
        status: "present",
        createdAt: "2024-11-22T07:45:00Z",
        updatedAt: "2024-11-22T18:15:00Z"
      },
      {
        id: "att_010",
        userId: "usr_promo_006",
        userRole: "promodizer",
        date: "2024-11-23T00:00:00Z",
        storeId: "store_004",
        clockInTime: "2024-11-23T09:00:00Z",
        clockOutTime: "2024-11-23T17:30:00Z",
        status: "present",
        createdAt: "2024-11-23T09:00:00Z",
        updatedAt: "2024-11-23T17:30:00Z"
      },
      {
        id: "att_011",
        userId: "usr_promo_001",
        userRole: "promodizer",
        date: "2024-11-24T00:00:00Z",
        storeId: "store_005",
        clockInTime: "2024-11-24T08:00:00Z",
        clockOutTime: null,
        status: "present",
        createdAt: "2024-11-24T08:00:00Z",
        updatedAt: "2024-11-24T08:00:00Z"
      },
      {
        id: "att_012",
        userId: "usr_promo_001",
        userRole: "promodizer",
        date: "2024-11-21T00:00:00Z",
        storeId: "store_001",
        clockInTime: "2024-11-21T08:00:00Z",
        clockOutTime: "2024-11-21T17:00:00Z",
        status: "present",
        createdAt: "2024-11-21T08:00:00Z",
        updatedAt: "2024-11-21T17:00:00Z"
      },
      {
        id: "att_013",
        userId: "usr_promo_002",
        userRole: "promodizer",
        date: "2024-11-21T00:00:00Z",
        storeId: "store_001",
        clockInTime: "2024-11-21T08:30:00Z",
        clockOutTime: "2024-11-21T16:30:00Z",
        status: "present",
        createdAt: "2024-11-21T08:30:00Z",
        updatedAt: "2024-11-21T16:30:00Z"
      },
      {
        id: "att_014",
        userId: "usr_sup_001",
        userRole: "supervisor",
        date: "2024-11-21T00:00:00Z",
        storeId: "store_001",
        clockInTime: "2024-11-21T07:30:00Z",
        clockOutTime: "2024-11-21T18:00:00Z",
        status: "present",
        createdAt: "2024-11-21T07:30:00Z",
        updatedAt: "2024-11-21T18:00:00Z"
      },
      {
        id: "att_015",
        userId: "usr_promo_003",
        userRole: "promodizer",
        date: "2024-11-22T00:00:00Z",
        storeId: "store_002",
        clockInTime: "2024-11-22T08:00:00Z",
        clockOutTime: "2024-11-22T17:00:00Z",
        status: "present",
        createdAt: "2024-11-22T08:00:00Z",
        updatedAt: "2024-11-22T17:00:00Z"
      },
      {
        id: "att_016",
        userId: "usr_promo_004",
        userRole: "promodizer",
        date: "2024-11-23T00:00:00Z",
        storeId: "store_003",
        clockInTime: "2024-11-23T08:00:00Z",
        clockOutTime: "2024-11-23T16:00:00Z",
        status: "present",
        createdAt: "2024-11-23T08:00:00Z",
        updatedAt: "2024-11-23T16:00:00Z"
      }
    ];

    // Store all collections in localStorage
    try {
      localStorage.setItem('users', JSON.stringify(users));
      localStorage.setItem('skus', JSON.stringify(skus));
      localStorage.setItem('stores', JSON.stringify(stores));
      localStorage.setItem('supervisorAllocations', JSON.stringify(supervisorAllocations));
      localStorage.setItem('promodizerAllocations', JSON.stringify(promodizerAllocations));
      localStorage.setItem('salesRecords', JSON.stringify(salesRecords));
      localStorage.setItem('attendanceRecords', JSON.stringify(attendanceRecords));

      // Mark initialization as complete
      localStorage.setItem('appInitialized', 'true');

      console.log('✅ App data successfully initialized in Local Storage!');
      console.log('📊 Data Summary:');
      console.log(`   - Users: ${users.length}`);
      console.log(`   - SKUs: ${skus.length}`);
      console.log(`   - Stores: ${stores.length}`);
      console.log(`   - Supervisor Allocations: ${supervisorAllocations.length}`);
      console.log(`   - Promodizer Allocations: ${promodizerAllocations.length}`);
      console.log(`   - Sales Records: ${salesRecords.length}`);
      console.log(`   - Attendance Records: ${attendanceRecords.length}`);
    } catch (error) {
      console.error('❌ Error initializing app data:', error);
    }
  }
};

AppData.init();