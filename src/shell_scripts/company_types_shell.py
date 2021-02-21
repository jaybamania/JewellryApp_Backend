from user.models import CompanyType
company_types = [
    'Branch Office',
    'Private Ltd Company',
    'Limited Liability Company',
    'Project Office',
    'Public Ltd Company',
    'Sole Proprietorship',
    'Unlimited Company',
    'Joint Hindu Family business',
    'Cooperatives',
    'Sole proprietorship',
    'Corporation',
    'Limited Liability Partnership(LLP)',
    'Subsidiary Company',
    'Partnership',
    'Liaison Office',
    'Limited'
]


for i in company_types:
    event = CompanyType(str(i))
    event.save()
